import { app, BrowserWindow, ipcMain } from 'electron';

function createWindow() {
    const win = new BrowserWindow({
        width: 400,
        height: 600,
        frame: false,
        transparent: true,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true
        },
        resizable: false,
        skipTaskbar: true,
        alwaysOnTop: true
    });

    // Animations fluides
    win.on('ready-to-show', () => {
        win.show();
        win.focus();
    });

    // Permet de déplacer le widget
    win.webContents.on('dom-ready', () => {
        win.webContents.insertCSS(`
            body { -webkit-app-region: drag; }
            input, button { -webkit-app-region: no-drag; }
        `);
    });

    win.loadURL('http://localhost:3000');
}


  app.whenReady().then(() => {
    createWindow()
  })

  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit()
    }
  })
