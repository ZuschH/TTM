; Toshiba Modbus Monitor (TMM) Windows installer
; This file is compiled by installer/build-installer.ps1 using Inno Setup 7.

#define AppName "Toshiba Modbus Monitor"
#define AppShortName "TMM"
#define AppVersion "1.0.0"
#define AppPublisher "TMM Project"
#define AppId "{{8D93850A-839D-48AC-AF45-271746A7612E}"

[Setup]
AppId={#AppId}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
VersionInfoVersion={#AppVersion}
DefaultDirName={autopf}\TMM
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
UsePreviousAppDir=yes
PrivilegesRequired=admin
SetupArchitecture=x64
ArchitecturesAllowed=x64compatible
MinVersion=10.0.17763
WizardStyle=modern
Compression=lzma2/max
SolidCompression=yes
OutputDir=output
OutputBaseFilename=TMM-Setup-{#AppVersion}
UninstallDisplayName={#AppName}
ChangesEnvironment=no
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "autostart"; Description: "Start TMM monitoring with Windows"; Flags: checkedonce
Name: "firewall"; Description: "Allow dashboard access from the private network"; Flags: checkedonce
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Dirs]
Name: "{commonappdata}\TMM"
Name: "{commonappdata}\TMM\logs"

; `staging` is created reproducibly by build-installer.ps1. Runtime and app
; remain separate so upgrades can replace binaries without touching ProgramData.
[Files]
Source: "staging\app\*"; DestDir: "{app}"; Excludes: "TMM-APP-MANIFEST.json"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "staging\runtime\*"; DestDir: "{app}\runtime"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "staging\app\TMM-APP-MANIFEST.json"; DestDir: "{app}"; Flags: ignoreversion; AfterInstall: VerifyInstalledApplication

[Icons]
Name: "{group}\Toshiba Modbus Monitor"; Filename: "http://localhost:8080/"
Name: "{autodesktop}\Toshiba Modbus Monitor"; Filename: "http://localhost:8080/"; Tasks: desktopicon
; The setup runs elevated. Use the common Startup folder so the tray controller
; starts in each interactive user's session rather than writing to the elevated
; install account's private profile.
Name: "{commonstartup}\Toshiba Modbus Monitor"; Filename: "{app}\runtime\pythonw.exe"; Parameters: """{app}\tmm_tray.pyw"""; WorkingDir: "{app}"

[Run]
Filename: "{app}\runtime\python.exe"; Parameters: """{app}\tmm_installer_config.py"" --config ""{commonappdata}\TMM\config.json"" --template ""{app}\config.example.json"" --device ""{code:GetSerialDevice}"" --baudrate {code:GetBaudrate} --model ""{code:GetModel}"" --name ""{code:GetDeviceName}"" --slave-id {code:GetSlaveId} --database ""{code:GetDatabasePath}"" --web-port {code:GetWebPort} --machine-speed-factor ""{code:GetMachineSpeedFactor}"" --machine-speed-unit ""{code:GetMachineSpeedUnit}"" --rated-output-current-a ""{code:GetRatedCurrent}"" --rated-output-voltage-v ""{code:GetRatedVoltage}"" --motor-rated-power-kw ""{code:GetMotorPower}"" --motor-rated-speed-rpm ""{code:GetMotorSpeed}"""; Flags: runhidden waituntilterminated; Check: not ConfigExists
Filename: "{app}\runtime\python.exe"; Parameters: """{app}\tmm_service.py"" --startup auto update"; Flags: runhidden waituntilterminated; Check: ServiceExists
Filename: "{app}\runtime\python.exe"; Parameters: """{app}\tmm_service.py"" --startup auto install"; Flags: runhidden waituntilterminated; Check: not ServiceExists
Filename: "{sys}\sc.exe"; Parameters: "config TMM start= auto"; Flags: runhidden waituntilterminated; Tasks: autostart
Filename: "{sys}\sc.exe"; Parameters: "config TMM start= demand"; Flags: runhidden waituntilterminated; Check: not ServiceAutostartSelected
Filename: "{sys}\sc.exe"; Parameters: "failure TMM reset= 86400 actions= restart/5000/restart/15000/restart/60000"; Flags: runhidden waituntilterminated
Filename: "{sys}\sc.exe"; Parameters: "failureflag TMM 1"; Flags: runhidden waituntilterminated
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -NonInteractive -Command ""Get-NetFirewallRule -DisplayName 'Toshiba Modbus Monitor Web' -ErrorAction SilentlyContinue | Remove-NetFirewallRule"""; Flags: runhidden waituntilterminated
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -NonInteractive -Command ""$port=(Get-Content -LiteralPath '{commonappdata}\TMM\config.json' -Raw | ConvertFrom-Json).web.port; New-NetFirewallRule -DisplayName 'Toshiba Modbus Monitor Web' -Direction Inbound -Action Allow -Protocol TCP -LocalPort $port -Profile Private | Out-Null"""; Flags: runhidden waituntilterminated; Tasks: firewall
Filename: "{sys}\sc.exe"; Parameters: "start TMM"; Flags: runhidden waituntilterminated
Filename: "{app}\runtime\pythonw.exe"; Parameters: """{app}\tmm_tray.pyw"""; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent; Description: "Start the TMM tray controller"

[UninstallRun]
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -NonInteractive -Command ""Get-CimInstance Win32_Process | Where-Object {{$_.CommandLine -like '*\TMM\tmm_tray.pyw*'} | ForEach-Object {{Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue}"""; Flags: runhidden waituntilterminated; RunOnceId: "StopTMMTray"
Filename: "{sys}\sc.exe"; Parameters: "stop TMM"; Flags: runhidden waituntilterminated; RunOnceId: "StopTMMService"
Filename: "{app}\runtime\python.exe"; Parameters: """{app}\tmm_service.py"" remove"; Flags: runhidden waituntilterminated; RunOnceId: "RemoveTMMService"
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -NonInteractive -Command ""Get-NetFirewallRule -DisplayName 'Toshiba Modbus Monitor Web' -ErrorAction SilentlyContinue | Remove-NetFirewallRule"""; Flags: runhidden waituntilterminated; RunOnceId: "RemoveTMMFirewall"
; Remove a database outside ProgramData as well, but only when the operator
; explicitly selected data removal in the uninstaller confirmation.
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -NonInteractive -Command ""$configPath='{commonappdata}\TMM\config.json'; if(Test-Path -LiteralPath $configPath) {{ $database=(Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json).storage.database; if($database) {{ Remove-Item -LiteralPath @($database,($database+'-wal'),($database+'-shm')) -Force -ErrorAction SilentlyContinue }} }}"""; Flags: runhidden waituntilterminated; RunOnceId: "RemoveTMMDatabase"; Check: DeleteTMMDataSelected

[UninstallDelete]
; Default behaviour retains this directory. It contains configuration, logs,
; archives and the default SQLite database.
Type: filesandordirs; Name: "{commonappdata}\TMM"; Check: DeleteTMMDataSelected

[Code]
var
  ConnectionPage: TWizardPage;
  EngineeringPage: TWizardPage;
  StoragePage: TWizardPage;
  SerialEdit: TNewEdit;
  BaudCombo: TNewComboBox;
  ModelCombo: TNewComboBox;
  DeviceNameEdit: TNewEdit;
  SlaveEdit: TNewEdit;
  DatabaseEdit: TNewEdit;
  DatabaseBrowseButton: TNewButton;
  WebPortEdit: TNewEdit;
  MachineFactorEdit: TNewEdit;
  MachineUnitEdit: TNewEdit;
  RatedCurrentEdit: TNewEdit;
  RatedVoltageEdit: TNewEdit;
  MotorPowerEdit: TNewEdit;
  MotorSpeedEdit: TNewEdit;
  LastSuggestedName: String;
  DeleteTMMData: Boolean;

function ConfigPath(): String;
begin
  Result := ExpandConstant('{commonappdata}\TMM\config.json');
end;

function ConfigExists(): Boolean;
begin
  Result := FileExists(ConfigPath());
end;

function DeleteTMMDataSelected(): Boolean;
begin
  Result := DeleteTMMData;
end;

function ServiceExists(): Boolean;
var
  ResultCode: Integer;
begin
  Result := Exec(ExpandConstant('{sys}\sc.exe'), 'query TMM', '', SW_HIDE,
    ewWaitUntilTerminated, ResultCode) and (ResultCode = 0);
end;

function ServiceAutostartSelected(): Boolean;
begin
  Result := WizardIsTaskSelected('autostart');
end;

procedure VerifyInstalledApplication();
var
  ResultCode: Integer;
begin
  if not Exec(ExpandConstant('{app}\runtime\python.exe'),
    '"' + ExpandConstant('{app}\tmm_verify_install.py') + '" --root "' +
    ExpandConstant('{app}') + '" --manifest "' +
    ExpandConstant('{app}\TMM-APP-MANIFEST.json') + '"',
    '', SW_HIDE, ewWaitUntilTerminated, ResultCode) or (ResultCode <> 0) then
    RaiseException('Installed TMM application files failed manifest verification.');
end;

function FirewallSelected(): Boolean;
begin
  Result := WizardIsTaskSelected('firewall');
end;

function GetSerialDevice(Param: String): String;
begin Result := Trim(SerialEdit.Text); end;
function GetBaudrate(Param: String): String;
begin Result := Trim(BaudCombo.Text); end;
function GetModel(Param: String): String;
begin Result := Trim(ModelCombo.Text); end;
function GetDeviceName(Param: String): String;
begin Result := Trim(DeviceNameEdit.Text); end;
function GetSlaveId(Param: String): String;
begin Result := Trim(SlaveEdit.Text); end;
function GetDatabasePath(Param: String): String;
begin Result := Trim(DatabaseEdit.Text); end;
function GetWebPort(Param: String): String;
begin Result := Trim(WebPortEdit.Text); end;
function GetMachineSpeedFactor(Param: String): String;
begin Result := Trim(MachineFactorEdit.Text); end;
function GetMachineSpeedUnit(Param: String): String;
begin Result := Trim(MachineUnitEdit.Text); end;
function GetRatedCurrent(Param: String): String;
begin Result := Trim(RatedCurrentEdit.Text); end;
function GetRatedVoltage(Param: String): String;
begin Result := Trim(RatedVoltageEdit.Text); end;
function GetMotorPower(Param: String): String;
begin Result := Trim(MotorPowerEdit.Text); end;
function GetMotorSpeed(Param: String): String;
begin Result := Trim(MotorSpeedEdit.Text); end;

function SuggestedDeviceName(Model: String): String;
begin
  if Model = 'VF-AS1' then Result := 'VFAS1-'
  else if Model = 'VF-AS3J' then Result := 'VFAS3-'
  else if Model = 'VF-S11' then Result := 'VFS11-'
  else if Model = 'VF-S15' then Result := 'VFS15-'
  else Result := '';
end;

procedure ModelChanged(Sender: TObject);
var
  NewSuggestion: String;
begin
  NewSuggestion := SuggestedDeviceName(ModelCombo.Text);
  if (Trim(DeviceNameEdit.Text) = '') or
     (DeviceNameEdit.Text = LastSuggestedName) then
    DeviceNameEdit.Text := NewSuggestion;
  LastSuggestedName := NewSuggestion;
end;

procedure BrowseDatabase(Sender: TObject);
var
  FileName: String;
  InitialDirectory: String;
begin
  FileName := Trim(DatabaseEdit.Text);
  InitialDirectory := ExtractFileDir(FileName);
  if not DirExists(InitialDirectory) then
    InitialDirectory := ExpandConstant('{commonappdata}');

  if GetSaveFileName(
    'Select or create the SQLite database',
    FileName,
    InitialDirectory,
    'SQLite databases (*.sqlite3)|*.sqlite3|All files (*.*)|*.*',
    'sqlite3') then begin
    if ExtractFileExt(FileName) = '' then
      FileName := FileName + '.sqlite3';
    DatabaseEdit.Text := FileName;
  end;
end;

procedure AddPageLabel(Page: TWizardPage; Caption: String; Top: Integer);
var
  PageLabel: TNewStaticText;
begin
  PageLabel := TNewStaticText.Create(Page);
  PageLabel.Parent := Page.Surface;
  PageLabel.Caption := Caption;
  PageLabel.Left := 0;
  PageLabel.Top := Top;
  PageLabel.AutoSize := True;
end;

procedure InitializeWizard();
begin
  ConnectionPage := CreateCustomPage(wpSelectDir,
    'Drive connection',
    'Configure the first inverter. Existing configurations are retained during upgrades.');

  AddPageLabel(ConnectionPage, 'COM port:', ScaleY(0));
  SerialEdit := TNewEdit.Create(ConnectionPage);
  SerialEdit.Parent := ConnectionPage.Surface;
  SerialEdit.SetBounds(0, ScaleY(18), ConnectionPage.SurfaceWidth, ScaleY(23));
  SerialEdit.Text := 'COM3';

  AddPageLabel(ConnectionPage, 'Baud rate:', ScaleY(50));
  BaudCombo := TNewComboBox.Create(ConnectionPage);
  BaudCombo.Parent := ConnectionPage.Surface;
  BaudCombo.Style := csDropDownList;
  BaudCombo.SetBounds(0, ScaleY(68), ConnectionPage.SurfaceWidth, ScaleY(23));
  BaudCombo.Items.Add('9600');
  BaudCombo.Items.Add('19200');
  BaudCombo.Items.Add('38400');
  BaudCombo.ItemIndex := 1;

  AddPageLabel(ConnectionPage, 'Inverter model:', ScaleY(100));
  ModelCombo := TNewComboBox.Create(ConnectionPage);
  ModelCombo.Parent := ConnectionPage.Surface;
  ModelCombo.Style := csDropDownList;
  ModelCombo.SetBounds(0, ScaleY(118), ConnectionPage.SurfaceWidth, ScaleY(23));
  ModelCombo.Items.Add('VF-AS1');
  ModelCombo.Items.Add('VF-AS3J');
  ModelCombo.Items.Add('VF-S11');
  ModelCombo.Items.Add('VF-S15');
  ModelCombo.ItemIndex := 0;
  ModelCombo.OnChange := @ModelChanged;

  AddPageLabel(ConnectionPage, 'Device name:', ScaleY(150));
  DeviceNameEdit := TNewEdit.Create(ConnectionPage);
  DeviceNameEdit.Parent := ConnectionPage.Surface;
  DeviceNameEdit.SetBounds(0, ScaleY(168), ConnectionPage.SurfaceWidth, ScaleY(23));
  LastSuggestedName := 'VFAS1-';
  DeviceNameEdit.Text := LastSuggestedName;

  AddPageLabel(ConnectionPage, 'Modbus address:', ScaleY(200));
  SlaveEdit := TNewEdit.Create(ConnectionPage);
  SlaveEdit.Parent := ConnectionPage.Surface;
  SlaveEdit.SetBounds(0, ScaleY(218), ConnectionPage.SurfaceWidth, ScaleY(23));
  SlaveEdit.Text := '1';

  EngineeringPage := CreateCustomPage(ConnectionPage.ID,
    'Engineering values',
    'Optional scaling and motor nameplate values. They can also be edited later in the dashboard.');
  AddPageLabel(EngineeringPage, 'Machine-speed factor:', ScaleY(0));
  MachineFactorEdit := TNewEdit.Create(EngineeringPage); MachineFactorEdit.Parent := EngineeringPage.Surface;
  MachineFactorEdit.SetBounds(0, ScaleY(18), ScaleX(220), ScaleY(23)); MachineFactorEdit.Text := '1.0';
  AddPageLabel(EngineeringPage, 'Machine-speed unit:', ScaleY(50));
  MachineUnitEdit := TNewEdit.Create(EngineeringPage); MachineUnitEdit.Parent := EngineeringPage.Surface;
  MachineUnitEdit.SetBounds(0, ScaleY(68), ScaleX(220), ScaleY(23)); MachineUnitEdit.Text := 'rpm';
  AddPageLabel(EngineeringPage, 'Rated output current (A, optional):', ScaleY(100));
  RatedCurrentEdit := TNewEdit.Create(EngineeringPage); RatedCurrentEdit.Parent := EngineeringPage.Surface;
  RatedCurrentEdit.SetBounds(0, ScaleY(118), ScaleX(220), ScaleY(23));
  AddPageLabel(EngineeringPage, 'Rated output voltage (V, optional):', ScaleY(150));
  RatedVoltageEdit := TNewEdit.Create(EngineeringPage); RatedVoltageEdit.Parent := EngineeringPage.Surface;
  RatedVoltageEdit.SetBounds(0, ScaleY(168), ScaleX(220), ScaleY(23));
  AddPageLabel(EngineeringPage, 'Motor rated power (kW, optional):', ScaleY(200));
  MotorPowerEdit := TNewEdit.Create(EngineeringPage); MotorPowerEdit.Parent := EngineeringPage.Surface;
  MotorPowerEdit.SetBounds(0, ScaleY(218), ScaleX(220), ScaleY(23));
  AddPageLabel(EngineeringPage, 'Motor rated speed (rpm, optional):', ScaleY(250));
  MotorSpeedEdit := TNewEdit.Create(EngineeringPage); MotorSpeedEdit.Parent := EngineeringPage.Surface;
  MotorSpeedEdit.SetBounds(0, ScaleY(268), ScaleX(220), ScaleY(23));

  StoragePage := CreateCustomPage(EngineeringPage.ID,
    'Storage and web interface',
    'Select the database location and local dashboard port.');
  AddPageLabel(StoragePage, 'Database file:', ScaleY(0));
  DatabaseEdit := TNewEdit.Create(StoragePage);
  DatabaseEdit.Parent := StoragePage.Surface;
  DatabaseEdit.SetBounds(0, ScaleY(18),
    StoragePage.SurfaceWidth - ScaleX(94), ScaleY(23));
  DatabaseEdit.Text := ExpandConstant('{commonappdata}\TMM\measurements.sqlite3');

  DatabaseBrowseButton := TNewButton.Create(StoragePage);
  DatabaseBrowseButton.Parent := StoragePage.Surface;
  DatabaseBrowseButton.Caption := 'Browse...';
  DatabaseBrowseButton.SetBounds(StoragePage.SurfaceWidth - ScaleX(86),
    ScaleY(17), ScaleX(86), ScaleY(25));
  DatabaseBrowseButton.OnClick := @BrowseDatabase;

  AddPageLabel(StoragePage, 'Web port:', ScaleY(58));
  WebPortEdit := TNewEdit.Create(StoragePage);
  WebPortEdit.Parent := StoragePage.Surface;
  WebPortEdit.SetBounds(0, ScaleY(76), StoragePage.SurfaceWidth, ScaleY(23));
  WebPortEdit.Text := '8080';
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := ((PageID = ConnectionPage.ID) or (PageID = EngineeringPage.ID) or (PageID = StoragePage.ID)) and
    ConfigExists();
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  Number: Integer;
  Device: String;
begin
  Result := True;
  if CurPageID = ConnectionPage.ID then begin
    Device := Uppercase(Trim(SerialEdit.Text));
    Number := StrToIntDef(Copy(Device, 4, Length(Device) - 3), -1);
    if (Length(Device) < 4) or (Copy(Device, 1, 3) <> 'COM') or
       (Number < 1) then begin
      MsgBox('Enter a valid Windows COM port, for example COM3.', mbError, MB_OK);
      Result := False; exit;
    end;
    if Trim(DeviceNameEdit.Text) = '' then begin
      MsgBox('Enter a device name.', mbError, MB_OK);
      Result := False; exit;
    end;
    Number := StrToIntDef(SlaveEdit.Text, -1);
    if (Number < 1) or (Number > 247) then begin
      MsgBox('Modbus address must be between 1 and 247.', mbError, MB_OK);
      Result := False; exit;
    end;
  end;
  if CurPageID = StoragePage.ID then begin
    if Trim(DatabaseEdit.Text) = '' then begin
      MsgBox('Enter a database file path.', mbError, MB_OK);
      Result := False; exit;
    end;
    Number := StrToIntDef(WebPortEdit.Text, -1);
    if (Number < 1) or (Number > 65535) then begin
      MsgBox('Web port must be between 1 and 65535.', mbError, MB_OK);
      Result := False; exit;
    end;
  end;
  if CurPageID = EngineeringPage.ID then begin
    if (Trim(MachineFactorEdit.Text) <> '') and (Trim(MachineUnitEdit.Text) = '') then begin
      MsgBox('Enter a machine-speed unit when a factor is configured.', mbError, MB_OK);
      Result := False; exit;
    end;
    if (Trim(MotorPowerEdit.Text) = '') <> (Trim(MotorSpeedEdit.Text) = '') then begin
      MsgBox('Motor rated power and speed must be entered together.', mbError, MB_OK);
      Result := False; exit;
    end;
  end;
end;

procedure StopTMMForUpgrade();
var
  ResultCode: Integer;
begin
  { Stop the service first and wait for the Service Control Manager.  On an
    upgrade, simply issuing "sc stop" is asynchronous: pythonservice.exe and
    its children can otherwise keep python3.dll open when [Files] starts. }
  Exec(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe'),
    '-NoProfile -NonInteractive -Command "$svc=Get-CimInstance Win32_Service -Filter ''Name=''''TMM'''''' -ErrorAction SilentlyContinue; if($svc) { Stop-Service -Name TMM -Force -ErrorAction SilentlyContinue; for($i=0;$i -lt 40;$i++) { $svc=Get-CimInstance Win32_Service -Filter ''Name=''''TMM'''''' -ErrorAction SilentlyContinue; if(!$svc -or $svc.State -eq ''Stopped'') { break }; Start-Sleep -Milliseconds 500 }; if($svc -and $svc.ProcessId -gt 0) { & $env:SystemRoot\System32\taskkill.exe /PID $svc.ProcessId /T /F | Out-Null } }; Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {{$_.CommandLine -like ''*\TMM\*''}} | ForEach-Object {{Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue}}; Start-Sleep -Milliseconds 1200"',
    '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssInstall then begin
    StopTMMForUpgrade();
  end;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
end;

function InitializeUninstall(): Boolean;
begin
  { Keep measurement data by default. In silent uninstallations data is also
    retained, because no interactive confirmation can be given. }
  DeleteTMMData := False;
  Result := True;
  if not UninstallSilent then begin
    DeleteTMMData := MsgBox(
      'Also delete all TMM data?' + #13#10 + #13#10 +
      'This permanently removes the configuration, logs, archives and the SQLite database. ' +
      'Choose Yes only when the recorded measurements are no longer needed.',
      mbConfirmation, MB_YESNO) = IDYES;
  end;
end;
