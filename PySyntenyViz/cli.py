import sys
import importlib


# Mapping of subcommands to their respective module paths
commands = {
    'change_origin': 'PySyntenyViz.change_gbk_origin',
    'revcomp': 'PySyntenyViz.gbk_rc',
    'reorder': 'PySyntenyViz.reorder_gbk',
    'synteny_viz': 'PySyntenyViz.synteny_viz',
    # Add more commands here
}


def main(args=None):
    if len(sys.argv) < 2:
        print("Usage: pysyntenyviz <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command in commands:
        # Import the appropriate module based on the command
        module = importlib.import_module(commands[command])
        
        # Call the main() function of the module, passing all remaining sys.argv arguments
        module.main(sys.argv[2:])  # Pass remaining arguments to module's main()
    else:
        print(f"Error: Unrecognized command '{command}'")
        print("Available commands:", ", ".join(commands.keys()))
        sys.exit(1)


if __name__ == "__main__":
    main()