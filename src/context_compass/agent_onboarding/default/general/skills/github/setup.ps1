#Requires -Version 5.1
<#
.SYNOPSIS
  Human-run standalone GitHub CLI Project setup (legacy helper, Windows).
.DESCRIPTION
  Run this yourself in an interactive PowerShell terminal. It takes a repository
  owner/name and a required GitHub Project URL, ensures the gh CLI is present
  and authenticated, refreshes the repo/project scopes gh needs, verifies the
  repository resolves, then hands detailed preflight to check_setup.py in this
  folder. It creates nothing in the repository and stores nothing itself.
  It refreshes repository and Project scopes for standalone CLI work. It is not
  required by the github_codex_plugin backend and does not authenticate that plugin.
  Authentication happens through `gh auth login --web` in your browser. Never
  paste a token into chat; gh keeps it in its own credential store, and this
  script never prints tokens or writes secrets to arguments, files, or logs.
.PARAMETER RepoOwner
  Repository owner (org or user). Prompted when omitted.
.PARAMETER RepoName
  Repository name. Prompted when omitted.
.PARAMETER ProjectUrl
  Required github.com Project URL (orgs/... or users/.../projects/<n>).
  This standalone Project helper always checks a Project. The YAML plugin
  backend permits an optional Project URL and does not run this helper.
.EXAMPLE
  .\setup.ps1 -RepoOwner octo-org -RepoName my-repo `
    -ProjectUrl https://github.com/orgs/octo-org/projects/3
#>
[CmdletBinding()]
param(
  [string]$RepoOwner = '',
  [string]$RepoName = '',
  [string]$ProjectUrl = ''
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$MinGhVersion = '2.83.2'

function Read-NonEmptyValue {
  param([string]$Current, [string]$Prompt)
  if ($Current -ne '') { return $Current }
  $answer = Read-Host $Prompt
  if ($answer -eq '') { throw "A value is required for: $Prompt" }
  return $answer
}

function Test-GhAvailable {
  $command = Get-Command gh -ErrorAction SilentlyContinue
  if ($null -eq $command) {
    throw 'gh CLI not found on PATH. Install it from https://cli.github.com, then re-run this script.'
  }
}

function Get-GhVersion {
  $firstLine = ((gh --version) | Select-Object -First 1)
  if ($firstLine -notmatch '^gh version (\d+)\.(\d+)\.(\d+)') {
    throw 'Could not parse `gh --version` output. Reinstall gh and retry.'
  }
  $found = "$($Matches[1]).$($Matches[2]).$($Matches[3])"
  if ([version]$found -lt [version]$MinGhVersion) {
    Write-Warning "gh $found is older than the supported floor $MinGhVersion. Continuing anyway; check_setup.py enforces the floor."
  } else {
    Write-Host "[ok] gh $found"
  }
}

function Ensure-GhAuth {
  gh auth status >$null 2>$null
  if ($LASTEXITCODE -ne 0) {
    Write-Host 'Opening browser authentication (gh auth login --web). Complete sign-in there; no token is shown here.'
    gh auth login --web
    if ($LASTEXITCODE -ne 0) { throw 'gh authentication did not complete.' }
  } else {
    Write-Host '[ok] gh authenticated'
  }
}

function Ensure-GhScopes {
# Refresh (never downgrade silently): repo read, org read, project write.
  # Interactive when the account needs to approve; nothing secret is echoed.
  gh auth refresh -s repo -s read:org -s project
  if ($LASTEXITCODE -ne 0) { throw 'Scope refresh did not complete. Re-run this script after reviewing the gh prompt.' }
  Write-Host '[ok] scopes refreshed (repo, read:org, project)'
}

function Test-RepoResolves {
  param([string]$Owner, [string]$Repo)
  $resolved = gh repo view "$Owner/$Repo" --json nameWithOwner --jq '.nameWithOwner'
  if ($LASTEXITCODE -ne 0) { throw "Repository '$Owner/$Repo' did not resolve. Check spelling and account access." }
  Write-Host "[ok] repository resolves: $resolved"
}

function Find-Python {
  foreach ($name in @('python3', 'python', 'py')) {
    $command = Get-Command $name -ErrorAction SilentlyContinue
    if ($null -ne $command) { return $command.Source }
  }
  throw 'No Python 3 interpreter found. Install Python 3.10+ and re-run this script.'
}

$RepoOwner = Read-NonEmptyValue $RepoOwner 'Repository owner (org or user)'
$RepoName = Read-NonEmptyValue $RepoName 'Repository name'
if ($ProjectUrl -eq '') {
  $ProjectUrl = Read-Host 'GitHub Project URL (required)'
}
if ($ProjectUrl -eq '') { throw 'A Project URL is required for this standalone CLI helper.' }

Test-GhAvailable
Get-GhVersion
Ensure-GhAuth
Ensure-GhScopes
Test-RepoResolves $RepoOwner $RepoName

$python = Find-Python
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$preflight = Join-Path $scriptRoot 'check_setup.py'
$arguments = @($preflight, '--owner', $RepoOwner, '--repo', $RepoName, '--project-url', $ProjectUrl)
& $python $arguments
if ($LASTEXITCODE -ne 0) { throw 'Preflight reported a problem; see its message above.' }
Write-Host 'Setup preflight passed. Nothing was created, modified, or stored by this script.'
