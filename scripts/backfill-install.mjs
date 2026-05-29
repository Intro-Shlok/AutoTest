/**
 * Backfill install field for all 215 tool markdown files.
 * Reads each file, determines install method(s), and writes the updated file.
 *
 * Usage: node scripts/backfill-install.mjs [--dry-run]
 */

import fs from "node:fs";
import path from "node:path";
import { glob } from "node:fs/promises";

const TOOLS_DIR = path.resolve("src/content/tools");

// ─── Known tool → install definitions ───────────────────────────────────────

const KNOWN_INSTALLS = {
  // ── System / coreutils ───────────────────────────────────────────────
  cat:          [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  rm:           [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  mv:           [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  cp:           [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  chmod:        [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  chown:        [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  ln:           [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  sort:         [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  uniq:         [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  wc:           [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  head:         [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  tail:         [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  tee:          [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  cut:          [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  tr:           [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }, { method: "brew", package_name: "coreutils", commands: ["brew install coreutils"] }],
  xargs:        [{ method: "apt", package_name: "findutils", commands: ["apt-get install -y findutils"] }, { method: "brew", package_name: "findutils", commands: ["brew install findutils"] }],
  find:         [{ method: "apt", package_name: "findutils", commands: ["apt-get install -y findutils"] }, { method: "brew", package_name: "findutils", commands: ["brew install findutils"] }],
  grep:         [{ method: "apt", package_name: "grep", commands: ["apt-get install -y grep"] }, { method: "brew", package_name: "grep", commands: ["brew install grep"] }],
  sed:          [{ method: "apt", package_name: "sed", commands: ["apt-get install -y sed"] }, { method: "brew", package_name: "gnu-sed", commands: ["brew install gnu-sed"] }],
  awk:          [{ method: "apt", package_name: "gawk", commands: ["apt-get install -y gawk"] }, { method: "brew", package_name: "gawk", commands: ["brew install gawk"] }],
  diff:         [{ method: "apt", package_name: "diffutils", commands: ["apt-get install -y diffutils"] }],
  comm:         [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }],
  strings:      [{ method: "apt", package_name: "binutils", commands: ["apt-get install -y binutils"] }, { method: "brew", package_name: "binutils", commands: ["brew install binutils"] }],
  hexdump:      [{ method: "apt", package_name: "bsdmainutils", commands: ["apt-get install -y bsdmainutils"] }],
  od:           [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }],
  xxd:          [{ method: "apt", package_name: "xxd", commands: ["apt-get install -y xxd"] }],
  dd:           [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }],
  stat:         [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }],
  df:           [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }],
  du:           [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }],
  free:         [{ method: "apt", package_name: "procps", commands: ["apt-get install -y procps"] }],
  timeout:      [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }],
  kill:         [{ method: "apt", package_name: "procps", commands: ["apt-get install -y procps"] }],
  ps:           [{ method: "apt", package_name: "procps", commands: ["apt-get install -y procps"] }],
  top:          [{ method: "apt", package_name: "procps", commands: ["apt-get install -y procps"] }],
  nice:         [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }],
  ionice:       [{ method: "apt", package_name: "util-linux", commands: ["apt-get install -y util-linux"] }],
  watch:        [{ method: "apt", package_name: "procps", commands: ["apt-get install -y procps"] }],
  make:         [{ method: "apt", package_name: "make", commands: ["apt-get install -y make"] }],
  patch:        [{ method: "apt", package_name: "patch", commands: ["apt-get install -y patch"] }],
  base64:       [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }],
  md5sum:       [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }],
  sha1sum:      [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }],
  sha256sum:    [{ method: "apt", package_name: "coreutils", commands: ["apt-get install -y coreutils"] }],
  tar:          [{ method: "apt", package_name: "tar", commands: ["apt-get install -y tar"] }],
  gzip:         [{ method: "apt", package_name: "gzip", commands: ["apt-get install -y gzip"] }],
  cron:         [{ method: "apt", package_name: "cron", commands: ["apt-get install -y cron"] }],
  journalctl:   [{ method: "apt", package_name: "systemd", commands: ["apt-get install -y systemd"] }],
  systemctl:    [{ method: "apt", package_name: "systemd", commands: ["apt-get install -y systemd"] }],
  mount:        [{ method: "apt", package_name: "mount", commands: ["apt-get install -y mount"] }],
  rsync:        [{ method: "apt", package_name: "rsync", commands: ["apt-get install -y rsync"] }],
  less:         [{ method: "apt", package_name: "less", commands: ["apt-get install -y less"] }],
  file:         [{ method: "apt", package_name: "file", commands: ["apt-get install -y file"] }],

  // ── Shells / languages ───────────────────────────────────────────────
  bash:         [{ method: "apt", package_name: "bash", commands: ["apt-get install -y bash"] }],
  python3:      [{ method: "apt", package_name: "python3", commands: ["apt-get install -y python3"] }],

  // ── Network essentials ───────────────────────────────────────────────
  curl:         [{ method: "apt", package_name: "curl", commands: ["apt-get install -y curl"] }, { method: "brew", package_name: "curl", commands: ["brew install curl"] }],
  wget:         [{ method: "apt", package_name: "wget", commands: ["apt-get install -y wget"] }, { method: "brew", package_name: "wget", commands: ["brew install wget"] }],
  ssh:          [{ method: "apt", package_name: "openssh-client", commands: ["apt-get install -y openssh-client"] }],
  scp:          [{ method: "apt", package_name: "openssh-client", commands: ["apt-get install -y openssh-client"] }],
  sftp:         [{ method: "apt", package_name: "openssh-client", commands: ["apt-get install -y openssh-client"] }],
  ftp:          [{ method: "apt", package_name: "ftp", commands: ["apt-get install -y ftp"] }],
  telnet:       [{ method: "apt", package_name: "telnet", commands: ["apt-get install -y telnet"] }],
  nc:           [{ method: "apt", package_name: "ncat", commands: ["apt-get install -y ncat"] }, { method: "brew", package_name: "nmap", commands: ["brew install nmap"] }],
  netcat:       [{ method: "apt", package_name: "netcat-openbsd", commands: ["apt-get install -y netcat-openbsd"] }],
  ifconfig:     [{ method: "apt", package_name: "net-tools", commands: ["apt-get install -y net-tools"] }],
  ip:           [{ method: "apt", package_name: "iproute2", commands: ["apt-get install -y iproute2"] }],
  route:        [{ method: "apt", package_name: "net-tools", commands: ["apt-get install -y net-tools"] }],
  ping:         [{ method: "apt", package_name: "iputils-ping", commands: ["apt-get install -y iputils-ping"] }],
  traceroute:   [{ method: "apt", package_name: "traceroute", commands: ["apt-get install -y traceroute"] }],
  dig:          [{ method: "apt", package_name: "dnsutils", commands: ["apt-get install -y dnsutils"] }],
  whois:        [{ method: "apt", package_name: "whois", commands: ["apt-get install -y whois"] }],
  openssl:      [{ method: "apt", package_name: "openssl", commands: ["apt-get install -y openssl"] }],
  git:          [{ method: "apt", package_name: "git", commands: ["apt-get install -y git"] }, { method: "brew", package_name: "git", commands: ["brew install git"] }],
  docker:       [{ method: "apt", package_name: "docker.io", commands: ["apt-get install -y docker.io"] }, { method: "brew", package_name: "docker", commands: ["brew install docker"] }],
  socat:        [{ method: "apt", package_name: "socat", commands: ["apt-get install -y socat"] }],
  "docker-compose": [{ method: "apt", package_name: "docker-compose", commands: ["apt-get install -y docker-compose"] }, { method: "brew", package_name: "docker-compose", commands: ["brew install docker-compose"] }],
  tcpdump:      [{ method: "apt", package_name: "tcpdump", commands: ["apt-get install -y tcpdump"] }, { method: "brew", package_name: "tcpdump", commands: ["brew install tcpdump"] }],
  iptables:     [{ method: "apt", package_name: "iptables", commands: ["apt-get install -y iptables"] }],

  // ── Network scanners / recon ──────────────────────────────────────────
  nmap:         [{ method: "apt", package_name: "nmap", commands: ["apt-get install -y nmap"] }, { method: "brew", package_name: "nmap", commands: ["brew install nmap"] }],
  masscan:      [{ method: "apt", package_name: "masscan", commands: ["apt-get install -y masscan"] }, { method: "git", repo_url: "https://github.com/robertdavidgraham/masscan", commands: ["git clone https://github.com/robertdavidgraham/masscan.git", "cd masscan && make && make install"] }],
  rustscan:     [{ method: "apt", package_name: "rustscan", commands: ["apt-get install -y rustscan"] }, { method: "cargo", package_name: "rustscan", commands: ["cargo install rustscan"] }],
  zmap:         [{ method: "apt", package_name: "zmap", commands: ["apt-get install -y zmap"] }],
  unicornscan:  [{ method: "apt", package_name: "unicornscan", commands: ["apt-get install -y unicornscan"] }],

  // ── Recon / OSINT ────────────────────────────────────────────────────
  amass:        [{ method: "apt", package_name: "amass", commands: ["apt-get install -y amass"] }, { method: "brew", package_name: "amass", commands: ["brew install amass"] }],
  subfinder:    [{ method: "go", repo_url: "github.com/projectdiscovery/subfinder/v2/cmd/subfinder", commands: ["go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"] }, { method: "apt", package_name: "subfinder", commands: ["apt-get install -y subfinder"] }],
  sublist3r:    [{ method: "pip", package_name: "sublist3r", commands: ["pip install sublist3r"] }],
  assetfinder:  [{ method: "go", repo_url: "github.com/tomnomnom/assetfinder", commands: ["go install github.com/tomnomnom/assetfinder@latest"] }],
  httpx:        [{ method: "go", repo_url: "github.com/projectdiscovery/httpx/cmd/httpx", commands: ["go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"] }],
  nuclei:       [{ method: "go", repo_url: "github.com/projectdiscovery/nuclei/v3/cmd/nuclei", commands: ["go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"] }],
  gau:          [{ method: "go", repo_url: "github.com/lc/gau", commands: ["go install github.com/lc/gau/v2/cmd/gau@latest"] }],
  katana:       [{ method: "go", repo_url: "github.com/projectdiscovery/katana/cmd/katana", commands: ["go install -v github.com/projectdiscovery/katana/cmd/katana@latest"] }],
  waybackurls:  [{ method: "go", repo_url: "github.com/tomnomnom/waybackurls", commands: ["go install github.com/tomnomnom/waybackurls@latest"] }],
  waymore:      [{ method: "git", repo_url: "https://github.com/xnl-h4ck3r/waymore", commands: ["git clone https://github.com/xnl-h4ck3r/waymore.git", "cd waymore && pip install -r requirements.txt"] }],
  dnsenum:      [{ method: "apt", package_name: "dnsenum", commands: ["apt-get install -y dnsenum"] }],
  dnsrecon:     [{ method: "apt", package_name: "dnsrecon", commands: ["apt-get install -y dnsrecon"] }, { method: "pip", package_name: "dnsrecon", commands: ["pip install dnsrecon"] }],
  fierce:       [{ method: "apt", package_name: "fierce", commands: ["apt-get install -y fierce"] }],
  "recon-ng":     [{ method: "apt", package_name: "recon-ng", commands: ["apt-get install -y recon-ng"] }],
  theHarvester:  [{ method: "apt", package_name: "theharvester", commands: ["apt-get install -y theharvester"] }],
  spiderfoot:   [{ method: "pip", package_name: "spiderfoot", commands: ["pip install spiderfoot"] }],
  shodan:       [{ method: "pip", package_name: "shodan", commands: ["pip install shodan"] }],
  censys:       [{ method: "pip", package_name: "censys", commands: ["pip install censys"] }],
  aquatone:     [{ method: "go", repo_url: "github.com/michenriksen/aquatone", commands: ["go install github.com/michenriksen/aquatone@latest"] }],
  whatweb:      [{ method: "apt", package_name: "whatweb", commands: ["apt-get install -y whatweb"] }],

  // ── Web app scanners ─────────────────────────────────────────────────
  ffuf:         [{ method: "go", repo_url: "github.com/ffuf/ffuf/v2", commands: ["go install github.com/ffuf/ffuf/v2@latest"] }, { method: "apt", package_name: "ffuf", commands: ["apt-get install -y ffuf"] }],
  gobuster:     [{ method: "go", repo_url: "github.com/OJ/gobuster/v3", commands: ["go install github.com/OJ/gobuster/v3@latest"] }, { method: "apt", package_name: "gobuster", commands: ["apt-get install -y gobuster"] }],
  dirsearch:    [{ method: "pip", package_name: "dirsearch", commands: ["pip install dirsearch"] }],
  feroxbuster:  [{ method: "apt", package_name: "feroxbuster", commands: ["apt-get install -y feroxbuster"] }, { method: "cargo", package_name: "feroxbuster", commands: ["cargo install feroxbuster"] }],
  nikto:        [{ method: "apt", package_name: "nikto", commands: ["apt-get install -y nikto"] }],
  wpscan:       [{ method: "apt", package_name: "wpscan", commands: ["apt-get install -y wpscan"] }],
  joomscan:     [{ method: "apt", package_name: "joomscan", commands: ["apt-get install -y joomscan"] }],
  cmsmap:       [{ method: "pip", package_name: "cmsmap", commands: ["pip install cmsmap"] }],
  sqlmap:       [{ method: "apt", package_name: "sqlmap", commands: ["apt-get install -y sqlmap"] }],
  sqlninja:     [{ method: "apt", package_name: "sqlninja", commands: ["apt-get install -y sqlninja"] }],
  commix:       [{ method: "apt", package_name: "commix", commands: ["apt-get install -y commix"] }],
  xsstrike:     [{ method: "pip", package_name: "xsstrike", commands: ["pip install xsstrike"] }],
  dalfox:       [{ method: "go", repo_url: "github.com/hahwul/dalfox/v2", commands: ["go install github.com/hahwul/dalfox/v2@latest"] }],
  crlfuzz:      [{ method: "go", repo_url: "github.com/dwisiswant0/crlfuzz", commands: ["go install github.com/dwisiswant0/crlfuzz/cmd/crlfuzz@latest"] }],
  paramspider:  [{ method: "pip", package_name: "paramspider", commands: ["pip install paramspider"] }],
  arjun:        [{ method: "pip", package_name: "arjun", commands: ["pip install arjun"] }],
  smuggler:     [{ method: "git", repo_url: "https://github.com/defparam/smuggler.git", commands: ["git clone https://github.com/defparam/smuggler.git"] }],
  "h2csmuggler": [{ method: "git", repo_url: "https://github.com/BishopFox/h2csmuggler.git", commands: ["git clone https://github.com/BishopFox/h2csmuggler.git"] }],
  dotdotpwn:    [{ method: "git", repo_url: "https://github.com/wireghoul/dotdotpwn.git", commands: ["git clone https://github.com/wireghoul/dotdotpwn.git"] }],
  kadimus:      [{ method: "git", repo_url: "https://github.com/P0cL4bs/kadimus.git", commands: ["git clone https://github.com/P0cL4bs/kadimus.git"] }],
  "lfi-suite":    [{ method: "git", repo_url: "https://github.com/D35m0nd142/LFISuite.git", commands: ["git clone https://github.com/D35m0nd142/LFISuite.git"] }],
  wfuzz:        [{ method: "apt", package_name: "wfuzz", commands: ["apt-get install -y wfuzz"] }, { method: "pip", package_name: "wfuzz", commands: ["pip install wfuzz"] }],
  hydra:        [{ method: "apt", package_name: "hydra", commands: ["apt-get install -y hydra"] }, { method: "brew", package_name: "hydra", commands: ["brew install hydra"] }],
  medusa:       [{ method: "apt", package_name: "medusa", commands: ["apt-get install -y medusa"] }],
  ncrack:       [{ method: "apt", package_name: "ncrack", commands: ["apt-get install -y ncrack"] }],
  patator:      [{ method: "apt", package_name: "patator", commands: ["apt-get install -y patator"] }],

  // ── Burp / ZAP ───────────────────────────────────────────────────────
  burpsuite:    [{ method: "custom", commands: ["wget -O burpsuite.sh https://portswigger.net/burp/releases/download?product=community&type=linux", "chmod +x burpsuite.sh && ./burpsuite.sh"] }],
  "owasp-zap":  [{ method: "apt", package_name: "zaproxy", commands: ["apt-get install -y zaproxy"] }],

  // ── Cracking / passwords ─────────────────────────────────────────────
  john:         [{ method: "apt", package_name: "john", commands: ["apt-get install -y john"] }, { method: "brew", package_name: "john", commands: ["brew install john"] }],
  hashcat:      [{ method: "apt", package_name: "hashcat", commands: ["apt-get install -y hashcat"] }, { method: "brew", package_name: "hashcat", commands: ["brew install hashcat"] }],
  "hash-identifier": [{ method: "pip", package_name: "hash-identifier", commands: ["pip install hash-identifier"] }],
  cewl:         [{ method: "apt", package_name: "cewl", commands: ["apt-get install -y cewl"] }],
  crunch:       [{ method: "apt", package_name: "crunch", commands: ["apt-get install -y crunch"] }],
  cupp:         [{ method: "apt", package_name: "cupp", commands: ["apt-get install -y cupp"] }],
  rsmangler:    [{ method: "apt", package_name: "rsmangler", commands: ["apt-get install -y rsmangler"] }],

  // ── Post-exploitation / C2 ───────────────────────────────────────────
  metasploit:   [{ method: "apt", package_name: "metasploit-framework", commands: ["curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod +x msfinstall && ./msfinstall"] }],
  empire:       [{ method: "git", repo_url: "https://github.com/BC-SECURITY/Empire.git", commands: ["git clone https://github.com/BC-SECURITY/Empire.git", "cd Empire && ./setup/install.sh"] }],
  covenant:     [{ method: "git", repo_url: "https://github.com/cobbr/Covenant.git", commands: ["git clone https://github.com/cobbr/Covenant.git"] }],
  havoc:        [{ method: "git", repo_url: "https://github.com/HavocFramework/Havoc.git", commands: ["git clone https://github.com/HavocFramework/Havoc.git", "cd Havoc && make"] }],
  mythic:       [{ method: "git", repo_url: "https://github.com/its-a-feature/Mythic.git", commands: ["git clone https://github.com/its-a-feature/Mythic.git", "cd Mythic && make"] }],
  sliver:       [{ method: "go", repo_url: "github.com/BishopFox/sliver", commands: ["go install github.com/BishopFox/sliver@latest"] }],
  merlin:       [{ method: "git", repo_url: "https://github.com/Ne0nd0g/merlin.git", commands: ["git clone https://github.com/Ne0nd0g/merlin.git"] }],
  pupy:         [{ method: "git", repo_url: "https://github.com/n1nj4sec/pupy.git", commands: ["git clone https://github.com/n1nj4sec/pupy.git"] }],
  veil:         [{ method: "git", repo_url: "https://github.com/Veil-Framework/Veil.git", commands: ["git clone https://github.com/Veil-Framework/Veil.git", "cd Veil && ./setup/install.sh"] }],
  shellter:     [{ method: "apt", package_name: "shellter", commands: ["apt-get install -y shellter"] }],
  setoolkit:    [{ method: "apt", package_name: "set", commands: ["apt-get install -y set"] }],
  beef:         [{ method: "apt", package_name: "beef-xss", commands: ["apt-get install -y beef-xss"] }],

  // ── AD / Windows internals ──────────────────────────────────────────
  impacket:     [{ method: "pip", package_name: "impacket", commands: ["pip install impacket"] }],
  mimikatz:     [{ method: "git", repo_url: "https://github.com/gentilkiwi/mimikatz.git", commands: ["git clone https://github.com/gentilkiwi/mimikatz.git"] }],
  rubeus:       [{ method: "git", repo_url: "https://github.com/GhostPack/Rubeus.git", commands: ["git clone https://github.com/GhostPack/Rubeus.git"] }],
  kerbrute:     [{ method: "go", repo_url: "github.com/ropnop/kerbrute", commands: ["go install github.com/ropnop/kerbrute@latest"] }],
  "evil-winrm": [{ method: "apt", package_name: "evil-winrm", commands: ["apt-get install -y evil-winrm"] }],
  "enum4linux-ng": [{ method: "pip", package_name: "enum4linux-ng", commands: ["pip install enum4linux-ng"] }],
  secretsdump:  [{ method: "pip", package_name: "impacket", commands: ["pip install impacket"] }],
  wmiexec:      [{ method: "pip", package_name: "impacket", commands: ["pip install impacket"] }],
  psexec:       [{ method: "pip", package_name: "impacket", commands: ["pip install impacket"] }],
  "NetExec (formerly CrackMapExec)": [{ method: "pip", package_name: "netexec", commands: ["pip install netexec"] }],
  netexec:      [{ method: "pip", package_name: "netexec", commands: ["pip install netexec"] }],
  BloodHound:   [{ method: "apt", package_name: "bloodhound", commands: ["apt-get install -y bloodhound"] }],
  sharphound:   [{ method: "git", repo_url: "https://github.com/BloodHoundAD/SharpHound.git", commands: ["git clone https://github.com/BloodHoundAD/SharpHound.git"] }],
  Certipy:      [{ method: "pip", package_name: "certipy-ad", commands: ["pip install certipy-ad"] }],
  ldapsearch:   [{ method: "apt", package_name: "ldap-utils", commands: ["apt-get install -y ldap-utils"] }],
  rpcclient:    [{ method: "apt", package_name: "samba-common-bin", commands: ["apt-get install -y samba-common-bin"] }],
  smbclient:    [{ method: "apt", package_name: "smbclient", commands: ["apt-get install -y smbclient"] }],
  smbmap:       [{ method: "pip", package_name: "smbmap", commands: ["pip install smbmap"] }],
  Responder:    [{ method: "apt", package_name: "responder", commands: ["apt-get install -y responder"] }],
  searchsploit: [{ method: "apt", package_name: "exploitdb", commands: ["apt-get install -y exploitdb"] }],

  // ── Wireless / Bluetooth ─────────────────────────────────────────────
  "aircrack-ng": [{ method: "apt", package_name: "aircrack-ng", commands: ["apt-get install -y aircrack-ng"] }],
  reaver:       [{ method: "apt", package_name: "reaver", commands: ["apt-get install -y reaver"] }],
  bully:        [{ method: "apt", package_name: "bully", commands: ["apt-get install -y bully"] }],
  wifite:       [{ method: "apt", package_name: "wifite", commands: ["apt-get install -y wifite"] }],
  kismet:       [{ method: "apt", package_name: "kismet", commands: ["apt-get install -y kismet"] }],
  bluetoothctl: [{ method: "apt", package_name: "bluez", commands: ["apt-get install -y bluez"] }],
  btlejack:     [{ method: "pip", package_name: "btlejack", commands: ["pip install btlejack"] }],
  hcxdumptool:  [{ method: "apt", package_name: "hcxdumptool", commands: ["apt-get install -y hcxdumptool"] }],
  hcxpcaptool:  [{ method: "apt", package_name: "hcxpcaptool", commands: ["apt-get install -y hcxpcaptool"] }],
  Yersinia:     [{ method: "apt", package_name: "yersinia", commands: ["apt-get install -y yersinia"] }],

  // ── Forensics / RE ───────────────────────────────────────────────────
  volatility:   [{ method: "pip", package_name: "volatility3", commands: ["pip install volatility3"] }],
  autopsy:      [{ method: "apt", package_name: "autopsy", commands: ["apt-get install -y autopsy"] }],
  binwalk:      [{ method: "apt", package_name: "binwalk", commands: ["apt-get install -y binwalk"] }],
  foremost:     [{ method: "apt", package_name: "foremost", commands: ["apt-get install -y foremost"] }],
  steghide:     [{ method: "apt", package_name: "steghide", commands: ["apt-get install -y steghide"] }],
  exiftool:     [{ method: "apt", package_name: "libimage-exiftool-perl", commands: ["apt-get install -y libimage-exiftool-perl"] }],
  gitleaks:     [{ method: "go", repo_url: "github.com/gitleaks/gitleaks", commands: ["go install github.com/gitleaks/gitleaks@latest"] }, { method: "brew", package_name: "gitleaks", commands: ["brew install gitleaks"] }],
  yara:         [{ method: "apt", package_name: "yara", commands: ["apt-get install -y yara"] }, { method: "brew", package_name: "yara", commands: ["brew install yara"] }],

  // ── Reverse engineering ──────────────────────────────────────────────
  gdb:          [{ method: "apt", package_name: "gdb", commands: ["apt-get install -y gdb"] }],
  radare2:      [{ method: "apt", package_name: "radare2", commands: ["apt-get install -y radare2"] }],
  cutter:       [{ method: "apt", package_name: "cutter", commands: ["apt-get install -y cutter"] }],
  ghidra:       [{ method: "git", repo_url: "https://github.com/NationalSecurityAgency/ghidra.git", commands: ["git clone https://github.com/NationalSecurityAgency/ghidra.git"] }],
  checksec:     [{ method: "pip", package_name: "checksec", commands: ["pip install checksec"] }],
  strace:       [{ method: "apt", package_name: "strace", commands: ["apt-get install -y strace"] }],
  ltrace:       [{ method: "apt", package_name: "ltrace", commands: ["apt-get install -y ltrace"] }],
  ropgadget:    [{ method: "pip", package_name: "ropgadget", commands: ["pip install ropgadget"] }],
  pwntools:     [{ method: "pip", package_name: "pwntools", commands: ["pip install pwntools"] }],
  scapy:        [{ method: "pip", package_name: "scapy", commands: ["pip install scapy"] }],

  // ── Traffic / MITM ──────────────────────────────────────────────────
  Wireshark:    [{ method: "apt", package_name: "wireshark", commands: ["apt-get install -y wireshark"] }],
  Ettercap:     [{ method: "apt", package_name: "ettercap-graphical", commands: ["apt-get install -y ettercap-graphical"] }],
  bettercap:    [{ method: "apt", package_name: "bettercap", commands: ["apt-get install -y bettercap"] }, { method: "go", repo_url: "github.com/bettercap/bettercap", commands: ["go install github.com/bettercap/bettercap@latest"] }],

  // ── SSL / TLS ────────────────────────────────────────────────────────
  sslscan:      [{ method: "apt", package_name: "sslscan", commands: ["apt-get install -y sslscan"] }],
  sslyze:       [{ method: "pip", package_name: "sslyze", commands: ["pip install sslyze"] }],
  "testssl.sh": [{ method: "git", repo_url: "https://github.com/drwetter/testssl.sh.git", commands: ["git clone https://github.com/drwetter/testssl.sh.git"] }],

  // ── Other ────────────────────────────────────────────────────────────
  chisel:       [{ method: "go", repo_url: "github.com/jpillora/chisel", commands: ["go install github.com/jpillora/chisel@latest"] }, { method: "brew", package_name: "chisel", commands: ["brew install chisel"] }],
  endlessh:     [{ method: "apt", package_name: "endlessh", commands: ["apt-get install -y endlessh"] }],
  loki:         [{ method: "git", repo_url: "https://github.com/Neo23x0/Loki.git", commands: ["git clone https://github.com/Neo23x0/Loki.git", "cd Loki && pip install -r requirements.txt"] }],
  slowhttptest: [{ method: "apt", package_name: "slowhttptest", commands: ["apt-get install -y slowhttptest"] }],

  // ── Text processing ─────────────────────────────────────────────────
  jq:           [{ method: "apt", package_name: "jq", commands: ["apt-get install -y jq"] }, { method: "brew", package_name: "jq", commands: ["brew install jq"] }],
  "tmux":       [{ method: "apt", package_name: "tmux", commands: ["apt-get install -y tmux"] }],

  // ── Web / cloud / mobile ─────────────────────────────────────────────
  "clairvoyance": [{ method: "git", repo_url: "https://github.com/noperator/clairvoyance.git", commands: ["git clone https://github.com/noperator/clairvoyance.git"] }],
  "ghauri":     [{ method: "pip", package_name: "ghauri", commands: ["pip install ghauri"] }],
  "tplmap":     [{ method: "git", repo_url: "https://github.com/epinna/tplmap.git", commands: ["git clone https://github.com/epinna/tplmap.git"] }],
  "jdam":       [{ method: "git", repo_url: "https://github.com/icebearr/JDAM.git", commands: ["git clone https://github.com/icebearr/JDAM.git"] }],
  "maltego":    [{ method: "apt", package_name: "maltego", commands: ["apt-get install -y maltego"] }],
  "unfurl":     [{ method: "go", repo_url: "github.com/tomnomnom/unfurl", commands: ["go install github.com/tomnomnom/unfurl@latest"] }],
  "routersploit": [{ method: "git", repo_url: "https://github.com/threat9/routersploit.git", commands: ["git clone https://github.com/threat9/routersploit.git", "cd routersploit && pip install -r requirements.txt"] }],
};

// ── Domain/namespace-based defaults ────────────────────────────────────────

const DOMAIN_DEFAULTS = {
  "system":         [{ method: "apt", package_name: null, commands: [] }],
  "network":        [{ method: "apt", package_name: null, commands: [] }],
  "container":      [{ method: "apt", package_name: null, commands: [] }],
  "text":           [{ method: "apt", package_name: null, commands: [] }],
  "internal":       [{ method: "apt", package_name: null, commands: [] }],
  "security:recon": [{ method: "go", package_name: null, commands: [] }],
  "security:web":   [{ method: "pip", package_name: null, commands: [] }],
  "security:crack": [{ method: "apt", package_name: null, commands: [] }],
  "security:exploit": [{ method: "git", repo_url: null, commands: [] }],
  "security:framework": [{ method: "pip", package_name: null, commands: [] }],
  "security:credential": [{ method: "git", repo_url: null, commands: [] }],
  "security:ad":    [{ method: "pip", package_name: null, commands: [] }],
  "security:wireless": [{ method: "apt", package_name: null, commands: [] }],
  "security:forensics": [{ method: "apt", package_name: null, commands: [] }],
  "security:reverse": [{ method: "apt", package_name: null, commands: [] }],
  "security":       [{ method: "git", package_name: null, commands: [] }],
};

function getDefaultInstall(name, namespace) {
  const domain = namespace ? namespace.split(":")[0] : "system";
  const nsPrefix = namespace ? namespace.split(":").slice(0, 2).join(":") : "";

  // Try 2-level namespace match first
  if (DOMAIN_DEFAULTS[nsPrefix]) {
    return [{ ...DOMAIN_DEFAULTS[nsPrefix][0], commands: guessCommands(name, DOMAIN_DEFAULTS[nsPrefix][0].method) }];
  }

  // Fall back to domain-level
  const def = DOMAIN_DEFAULTS[domain];
  if (def) return [{ ...def[0], commands: guessCommands(name, def[0].method) }];

  return [{ method: "apt", package_name: name.toLowerCase().replace(/\s+/g, "-"), commands: guessCommands(name, "apt") }];
}

function guessCommands(name, method) {
  const safeName = name.toLowerCase().replace(/[^a-z0-9.\-_]/g, "-").replace(/-+/g, "-");
  switch (method) {
    case "apt":
      return [`apt-get install -y ${safeName}`];
    case "brew":
      return [`brew install ${safeName}`];
    case "pip":
      return [`pip install ${safeName}`];
    case "pipx":
      return [`pipx install ${safeName}`];
    case "go":
      return [`go install github.com/${safeName}@latest`];
    case "cargo":
      return [`cargo install ${safeName}`];
    case "npm":
      return [`npm install -g ${safeName}`];
    case "gem":
      return [`gem install ${safeName}`];
    case "snap":
      return [`snap install ${safeName}`];
    case "git":
      return [`git clone https://github.com/${safeName}/${safeName}.git`];
    default:
      return [`apt-get install -y ${safeName}`];
  }
}

// ─── Main ──────────────────────────────────────────────────────────────────

async function main() {
  const dryRun = process.argv.includes("--dry-run");
  let updated = 0;
  let skipped = 0;

  for await (const filePath of glob("**/*.md", { cwd: TOOLS_DIR, root: TOOLS_DIR })) {
    const fullPath = path.join(TOOLS_DIR, filePath);
    const raw = fs.readFileSync(fullPath, "utf-8");

    // Parse frontmatter manually (simple approach) or use gray-matter
    const match = raw.match(/^---\n([\s\S]*?)\n---\n/);
    if (!match) { skipped++; continue; }

    const frontmatter = match[1];
    const body = raw.slice(match[0].length);

    // Extract name
    const nameMatch = frontmatter.match(/^name:\s*(.+)$/m);
    if (!nameMatch) { skipped++; continue; }
    const name = nameMatch[1].trim();

    const nsMatch = frontmatter.match(/^namespace:\s*(.+)$/m);
    const namespace = nsMatch ? nsMatch[1].trim() : "unknown:unknown";

    // Check if install field already exists
    if (frontmatter.includes("install:")) {
      skipped++;
      continue;
    }

    // Skip index.md (the repo overview page)
    if (filePath === "index.md" || name === "AutoTest Knowledge Repository") {
      skipped++;
      continue;
    }

    // Get install definition
    const install = KNOWN_INSTALLS[name] || getDefaultInstall(name, namespace);

    // Build the YAML for install field
    const installYaml = install.map(inst => {
      const lines = [`    - method: ${inst.method}`];
      if (inst.package_name) lines.push(`      package_name: "${inst.package_name}"`);
      if (inst.repo_url) lines.push(`      repo_url: "${inst.repo_url}"`);
      if (inst.commands && inst.commands.length > 0) {
        const cmdYaml = inst.commands.map(c => `        - "${c.replace(/"/g, '\\"')}"`).join("\n");
        lines.push(`      commands:\n${cmdYaml}`);
      } else {
        const guessed = guessCommands(name, inst.method);
        const cmdYaml = guessed.map(c => `        - "${c.replace(/"/g, '\\"')}"`).join("\n");
        lines.push(`      commands:\n${cmdYaml}`);
      }
      return lines.join("\n");
    }).join("\n");

    const installBlock = `install:\n${installYaml}`;

    // Insert install field before the closing ---
    const updatedFrontmatter = frontmatter + "\n" + installBlock;
    const updatedContent = "---\n" + updatedFrontmatter + "\n---\n" + body;

    if (dryRun) {
      console.log(`[DRY-RUN] Would update: ${filePath} (${name})`);
    } else {
      fs.writeFileSync(fullPath, updatedContent);
    }
    updated++;
  }

  console.log(`\nDone. ${updated} files updated, ${skipped} skipped.`);
}

main().catch(err => { console.error(err); process.exit(1); });
