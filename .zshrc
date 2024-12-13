echo '
function clean_and_execute() {
    while IFS= read -r line; do
        command="${line#*% }"
        if [[ -n "$command" ]]; then
            eval "$command"
        fi
    done
}' >> ~/.zshrc