import { useEffect } from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import useAuthStore from '../utils/auth';
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  const initialize = useAuthStore((state) => state.initialize);
  
  useEffect(() => {
    initialize();
  }, [initialize]);

  return (
    <>
      <Component {...pageProps} />
      <ToastContainer position="top-right" autoClose={5000} />
    </>
  );
}

export default MyApp;