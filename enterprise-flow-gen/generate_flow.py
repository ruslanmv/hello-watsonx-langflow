#!/usr/bin/env python3
"""
Universal CrewAI Flow Generator - Entry Point

This script compiles YAML configuration files into a Langflow JSON file.

Usage:
    python generate_flow.py [output_file]

Arguments:
    output_file: Optional path to output JSON file (default: enterprise_demo.json)

Example:
    python generate_flow.py
    python generate_flow.py my_custom_flow.json
"""

import sys
import argparse
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.compiler import FlowCompiler


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Universal CrewAI Flow Generator for Langflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_flow.py
  python generate_flow.py my_flow.json
  python generate_flow.py --config ./my_configs --output ./output/flow.json

Configuration Files Required:
  - config/tools_mcp.yaml  (MCP Servers & Custom Tools)
  - config/agents.yaml     (CrewAI Agents)
  - config/tasks.yaml      (CrewAI Tasks)

Output:
  A Langflow-compatible JSON file ready for import.
        """
    )

    parser.add_argument(
        "output_file",
        nargs="?",
        default="enterprise_demo.json",
        help="Output JSON file path (default: enterprise_demo.json)"
    )

    parser.add_argument(
        "--config",
        "-c",
        default="config",
        help="Configuration directory path (default: config)"
    )

    parser.add_argument(
        "--output",
        "-o",
        dest="output_file_flag",
        help="Output JSON file path (alternative to positional argument)"
    )

    parser.add_argument(
        "--validate-only",
        "-v",
        action="store_true",
        help="Only validate configuration without generating output"
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress all output except errors"
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Determine output file
    output_file = args.output_file_flag or args.output_file

    if not args.quiet:
        print("\n" + "=" * 60)
        print("UNIVERSAL CREWAI FLOW GENERATOR")
        print("Enterprise AI Architect & Python Tooling")
        print("=" * 60 + "\n")

    try:
        # Initialize compiler
        compiler = FlowCompiler(config_dir=args.config)

        # Load configurations
        compiler.load_configs()

        # Validate
        compiler.validate_config()

        if args.validate_only:
            print("\n✅ Configuration is valid!")
            print("\nTo generate the flow, run without --validate-only flag.")
            return 0

        # Compile
        flow = compiler.compile()

        # Export
        compiler.export_json(flow, output_file)

        if not args.quiet:
            print("\n" + "=" * 60)
            print("🎉 SUCCESS!")
            print("=" * 60)
            print(f"\nYour Langflow JSON is ready: {Path(output_file).absolute()}")
            print("\nNext steps:")
            print("  1. Open Langflow in your browser")
            print("  2. Click 'Import' and select the generated JSON file")
            print("  3. Review and customize the flow")
            print("  4. Run your enterprise AI workflow!")
            print()

        return 0

    except FileNotFoundError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure all required YAML files exist:")
        print(f"  - {args.config}/tools_mcp.yaml")
        print(f"  - {args.config}/agents.yaml")
        print(f"  - {args.config}/tasks.yaml")
        return 1

    except Exception as e:
        print(f"\n❌ Error: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
