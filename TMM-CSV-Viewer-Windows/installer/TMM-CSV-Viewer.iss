#define AppName "TMM CSV Viewer"
#define AppVersion "1.0.0"
#define AppId "{{89B56912-17EC-4D72-953C-277B4E43D7D7}"

[Setup]
AppId={#AppId}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
DefaultDirName={autopf}\TMM CSV Viewer
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
PrivilegesRequired=admin
SetupArchitecture=x64
ArchitecturesAllowed=x64compatible
MinVersion=10.0.17763
WizardStyle=modern
Compression=lzma2/max
SolidCompression=yes
OutputDir=output
OutputBaseFilename=TMM-CSV-Viewer-Setup-{#AppVersion}
CloseApplications=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Files]
Source: "staging\app\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "staging\runtime\*"; DestDir: "{app}\runtime"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\TMM CSV Viewer"; Filename: "{app}\runtime\pythonw.exe"; Parameters: """{app}\tmm_csv_viewer.pyw"""; WorkingDir: "{app}"
Name: "{autodesktop}\TMM CSV Viewer"; Filename: "{app}\runtime\pythonw.exe"; Parameters: """{app}\tmm_csv_viewer.pyw"""; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\runtime\pythonw.exe"; Parameters: """{app}\tmm_csv_viewer.pyw"""; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent; Description: "Start TMM CSV Viewer"
