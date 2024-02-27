 labels.next()
    targets = ["zsh", "powerline"]
    result = run_many_arguments(cmd, targets)
    if result == PASS:
        repo = "https://raw.githubusercontent.com/ohmyzsh/"
        install_omz = f"{repo}ohmyzsh/master/tools/install.sh"
        result = run_shell_script(script=install_omz, shell="sh")
    if result == PASS:
        src = "https://github.com/romkatv/powerlevel10k.git"
        dest = "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"
        p10k_cmd = f"git clone --depth=1 {src} {dest}"
        result = run_one_command(cmd=p10k_cmd)
    print(result)
