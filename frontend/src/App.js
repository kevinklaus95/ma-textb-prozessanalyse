import React from 'react';
import './App.css';
import Root from './root'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

// Hier wird die App initialisiert sowie der Material-UI Provider und der Header der App gesetzt.
function App() {
  return (
    <div className="App">
      <MuiThemeProvider>
      <header className="App-header">
        Textbasierte Prozessanalyse
      </header>
      <Root />
        </MuiThemeProvider>
    </div>
  );
}

export default App;
