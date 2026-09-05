import React, { Component } from 'react';
import { AlertCircle } from 'lucide-react';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo); fetch("http://localhost:9999/log", { method: "POST", body: error.toString() + " | " + (error.stack || "") }).catch(e => console.log(e));
  }

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      const lang = localStorage.getItem('italienation_lang') || 'it';
      
      const title = lang === 'it' ? 'Qualcosa è andato storto' : 'Something went wrong';
      const message = lang === 'it' 
        ? 'Si è verificato un errore inaspettato durante il caricamento.' 
        : 'An unexpected error occurred while loading this page.';
      const buttonText = lang === 'it' ? 'Ricarica pagina' : 'Reload page';

      return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
          <div className="bg-zinc-900 p-8 rounded-2xl border border-red-500/20 flex flex-col items-center max-w-md w-full shadow-2xl">
            <div className="w-16 h-16 bg-red-500/10 text-red-500 rounded-full flex items-center justify-center mb-6">
              <AlertCircle size={32} />
            </div>
            <h1 className="text-xl font-bold text-white mb-2">{title}</h1>
            <p className="text-zinc-400 mb-8">{message}</p><p className="text-red-400 font-mono text-sm mb-4">{this.state.error && this.state.error.toString()}</p>
            <button 
              onClick={this.handleReload}
              className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl transition font-medium w-full"
            >
              {buttonText}
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
