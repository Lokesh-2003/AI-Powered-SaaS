import { Doughnut, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

export default function AnalysisDashboard({ resume }) {
  if (!resume.analysis_result) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <p className="text-gray-500">Analysis not available</p>
      </div>
    );
  }

  const analysis = typeof resume.analysis_result === 'string' 
    ? JSON.parse(resume.analysis_result) 
    : resume.analysis_result;

  const skillsData = {
    labels: analysis.skills.slice(0, 10),
    datasets: [
      {
        data: analysis.skills.slice(0, 10).map(() => Math.floor(Math.random() * 100) + 1),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
          '#FF9F40', '#8AC24A', '#607D8B', '#E91E63', '#3F51B5'
        ],
      }
    ]
  };

  const keywordData = {
    labels: Object.keys(analysis.keyword_scores || {}),
    datasets: [
      {
        label: 'Keyword Relevance',
        data: Object.values(analysis.keyword_scores || {}),
        backgroundColor: '#3B82F6',
      }
    ]
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow space-y-6">
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">{resume.filename}</h3>
        <p className="text-sm text-gray-500">Uploaded on {new Date(resume.upload_date).toLocaleDateString()}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-medium text-gray-900 mb-3">Top Skills</h4>
          <Doughnut data={skillsData} />
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-medium text-gray-900 mb-3">Keyword Analysis</h4>
          <Bar 
            data={keywordData} 
            options={{
              scales: {
                y: {
                  beginAtZero: true,
                  max: 1
                }
              }
            }} 
          />
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <h4 className="font-medium text-gray-900 mb-2">Experience</h4>
          <ul className="list-disc pl-5 space-y-1">
            {analysis.experience?.slice(0, 5).map((item, index) => (
              <li key={index} className="text-sm text-gray-700">{item}</li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="font-medium text-gray-900 mb-2">Education</h4>
          <ul className="list-disc pl-5 space-y-1">
            {analysis.education?.slice(0, 3).map((item, index) => (
              <li key={index} className="text-sm text-gray-700">{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}