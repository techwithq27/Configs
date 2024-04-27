export PATH=$PATH:"/usr/local/go/bin:/home/quentinh/.bin:/home/quentinh/.cargo/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/snap/bin:/home/quentinh/.local/bin:/home/quentinh/.config/emacs/bin"
alias emacs="emacsclient -c -a 'emacs'"
alias up2="sudo apt update && sudo apt upgrade -y"
alias wk="sudo openvpn --config /home/quentinh/Notes/OE-T3VPN.ovpn --data-ciphers AES-128-CBC"
alias it="sudo apt install"
alias ui="sudo apt purge"
alias jump="ssh ash-sys-pro-js4"
alias search="sudo apt search"
alias lookup="rpm -qa"
#alias bitwarden="/var/lib/flatpak/app/com.bitwarden.desktop/x86_64/stable/active/files/Bitwarden/bitwarden &"
#alias slack="/var/lib/flatpak/app/com.slack.Slack/x86_64/stable/active/files/bin/slack"
#alias obsidian="/var/lib/flatpak/exports/bin/md.obsidian.Obsidian &"
alias sk="sudo killall -9"
alias mip="curl icanhazip.com"
alias cwp="ssh -p 9559 -i /home/quentinh/.ssh/cwp cwptech5@70.39.250.3"
alias cpvps="ssh -p 8558 -i /home/quentinh/.ssh/alma techque@173.231.198.201"
alias work_up="openvpn3 session-start --config BigVPN"
alias work_down="openvpn3 session-manage --config BigVPN --disconnect"
alias bwk="sudo openvpn --config /home/quentinh/Notes/Systemsbigvpn2.ovpn"
alias espanso_restart="espanso stop && killall -9 espanso && espanso service unregister && espanso service register && espanso start"
alias vim="nvim"
function cd() {

	builtin cd "$1"
	ls -ACF
}

function op() {

	openssl s_client -connect $1:$2

}
