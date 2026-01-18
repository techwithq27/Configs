import os

import libqtile.resources
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras.widget.decorations import RectDecoration


mod = "mod4"
terminal = "konsole"
browser = "vivaldi-stable"
editor = "hx"
def autostart():
    subprocess.Popen([os.path.expanduser("~/.config/qtile/autostart.sh")])




def _wm_class_matches(win, target: str) -> bool:
    # Ignore Qtile internal windows (bar, systray, etc.)
    try:
        wm_class = win.get_wm_class()
    except Exception:
        return False

    if not wm_class:
        return False

    t = target.lower()
    return any(t == c.lower() or t in c.lower() for c in wm_class)

def goto_or_spawn(cmd: str, wm_class: str):
    @lazy.function
    def _inner(qtile):
        for w in qtile.windows_map.values():
            if _wm_class_matches(w, wm_class):
                # jump to the group the window is on
                if w.group:
                    w.group.toscreen()
                w.focus(warp=True)
                try:
                    w.bring_to_front()
                except Exception:
                    pass
                return
        qtile.cmd_spawn(cmd)
    return _inner




keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    
    ## Custom key bindings
    Key([mod], "Return", lazy.spawn(terminal), desc="Terminal (Ghostty)"),
    Key([mod], "b", goto_or_spawn("vivaldi-stable", "Vivaldi-stable"), desc="Browser (Vivaldi)"),
    Key([mod], "e", lazy.spawn(editor), desc="Editor (Helix)"),    
    Key(["mod1"], "c", lazy.spawn("copyq toggle"), desc="lipboard"),
    Key(["mod1"], "r", lazy.spawn("rofi -show drun"), desc="Runner" ),


    Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume -l 1.5 @DEFAULT_AUDIO_SINK@ 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-")),
    Key([], "XF86AudioMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "x", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    Key([mod, "control"], "l", lazy.spawn("i3lock -c 000000"), desc="Lock screen"),
    Key([mod, "mod1"],"t" , lazy.hide_show_bar("top"), desc="Toggle top bar"),
    
    KeyChord(["mod1"], "v", [
        Key([], "Right", lazy.spawn("variety --next"), desc="Next wallpaper"),
        Key([], "Left",  lazy.spawn("variety --previous"), desc="Previous wallpaper"),
    ], name="variety")
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
#for vt in range(1, 8):
#    keys.append(
  #      Key(
  #          ["control", "mod1"],
  #          f"f{vt}",
  #          lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
  #          desc=f"Switch to VT{vt}",
  #      )
  #  )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
     layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="fira code",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

pill = [
    RectDecoration(
        colour="#1e1e1ecc",  # translucent dark
        radius=12,
        filled=True,
        padding_y=6,
        padding_x=10,
        group=True,
    )
]

#logo = os.path.join(os.path.dirname(libqtile.resources.__file__), "logo.png")
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(foreground="#ffff00"),
                widget.GroupBox(decorations=pill, padding=6, foreground="#ffff00"),
                widget.Prompt(foreground="#ffff00"),
                widget.Spacer(),
                widget.Clock(decorations=pill, format="%I:%M %p", foreground="#ffff00"),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TaskList(decorations=pill, foreground="#ffff00"),
                widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#ffff00"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.QuickExit(foreground="#ffff00"),
            ],
            size=32,
            background="#191970",
            margin=[10, 20, 0, 20],   # top, right, bottom, left
            reserve=False,
            #24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
       # background="#000000",
       # wallpaper=logo,
       # wallpaper_mode="center",
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]


def float_and_place_copyq(window):
    try:
        wm_class = window.get_wm_class() or []
    except Exception:
        return
    if any("copyq" in c.lower() for c in wm_class):
        window.floating = True
        window.place(50, 50, 900, 600, 2, None)  # x, y, w, h, border, bordercolor
        window.bring_to_front()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

idle_inhibitors = []  # type: list

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
