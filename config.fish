if status is-interactive
    #set -g theme_display_user ssh
    #set -g theme_color_scheme dark
    #set -g theme_git_worktree_support yes
    #set -g theme_display_git yes
    #set -g theme_nerd_fonts yes
    #set -g theme_powerline_fonts yes
    if test -e /home/quentinh/.fish_alias.fish
        source /home/quentinh/.fish_alias.fish
    end
    pfetch
    # Commands to run in interactive sessions can go here
end
