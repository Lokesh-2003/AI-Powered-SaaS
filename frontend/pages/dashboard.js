import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import useAuthStore from '../utils/auth';
import { uploadResume, getResumes } from '../utils/api';
import DashboardLayout from '../components/DashboardLayout';
import ResumeUploadForm from '../components/ResumeUploadForm';
import ResumeList from '../components/ResumeList';
import AnalysisDashboard from '../components/AnalysisDashboard';
import { toast } from 'react-toastify';

export default function Dashboard() {
  const router = useRouter();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const [resumes, setResumes] = useState([]);
  const [selectedResume, setSelectedResume] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    } else {
      fetchResumes();
    }
  }, [isAuthenticated, router]);

  const fetchResumes = async () => {
    try {
      setLoading(true);
      const data = await getResumes();
      setResumes(data);
      if (data.length > 0 && !selectedResume) {
        setSelectedResume(data[0]);
      }
    } catch (error) {
      toast.error('Failed to fetch resumes');
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (file) => {
    try {
      setLoading(true);
      const newResume = await uploadResume(file);
      setResumes([newResume, ...resumes]);
      setSelectedResume(newResume);
      toast.success('Resume uploaded successfully!');
    } catch (error) {
      toast.error('Failed to upload resume');
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) return null;

  return (
    <DashboardLayout>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ResumeUploadForm onUpload={handleUpload} loading={loading} />
          <ResumeList 
            resumes={resumes} 
            selectedId={selectedResume?.id} 
            onSelect={setSelectedResume} 
            loading={loading}
          />
        </div>
        <div className="lg:col-span-2">
          {selectedResume ? (
            <AnalysisDashboard resume={selectedResume} />
          ) : (
            <div className="bg-white p-6 rounded-lg shadow">
              <p className="text-gray-500">Select a resume to view analysis</p>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}