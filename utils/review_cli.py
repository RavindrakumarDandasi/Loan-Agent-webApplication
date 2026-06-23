"""
CLI tool for evaluating case study submissions.
Usage: python -m utils.review_cli --participant-name "Name" --submission-path "/path/to/submission" --output-file "./report.md"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.evaluator import SubmissionEvaluator


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate GEN-AI case study submissions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Evaluate current project:
    python -m utils.review_cli --participant-name "John Doe" --submission-path "."

  Evaluate and save report:
    python -m utils.review_cli --participant-name "Jane Smith" --submission-path "./submission" --output-file "./reports/jane_eval.md"

  Evaluate with default output filename:
    python -m utils.review_cli --participant-name "Bob Johnson" --submission-path "./solutions/bob"
        """
    )

    parser.add_argument(
        "--participant-name",
        "-n",
        required=True,
        help="Name of the participant (required)"
    )

    parser.add_argument(
        "--submission-path",
        "-p",
        required=True,
        help="Path to the submission folder (required)"
    )

    parser.add_argument(
        "--output-file",
        "-o",
        help="Output file path for the report (optional, defaults to 'evaluation_<participant_name>.md')"
    )

    parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )

    args = parser.parse_args()

    # Validate submission path
    submission_path = Path(args.submission_path)
    if not submission_path.exists():
        print(f"Error: Submission path does not exist: {submission_path}")
        sys.exit(1)

    if not submission_path.is_dir():
        print(f"Error: Submission path must be a directory: {submission_path}")
        sys.exit(1)

    # Determine output file path
    if args.output_file:
        output_file = Path(args.output_file)
    else:
        safe_name = args.participant_name.lower().replace(" ", "_")
        ext = "json" if args.format == "json" else "md"
        output_file = Path(f"evaluation_{safe_name}.{ext}")

    # Run evaluation
    print(f"Evaluating submission for: {args.participant_name}")
    print(f"Submission path: {submission_path}")

    evaluator = SubmissionEvaluator()
    report = evaluator.evaluate(
        submission_path=str(submission_path.absolute()),
        participant_name=args.participant_name
    )

    # Save report
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "json":
        import json
        with open(output_file, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)
    else:
        with open(output_file, 'w') as f:
            f.write(report.to_markdown())

    print(f"✓ Report saved to: {output_file.absolute()}")
    print(f"\nEvaluation Summary:")
    print(f"  Overall Score: {report.overall_score}/10")
    print(f"  Grade: {report.grade}")
    print(f"  Status: {report.status}")
    print(f"  Completion: {'✓ Complete' if report.completion_check.is_complete else '✗ Incomplete'}")

    if not report.completion_check.is_complete:
        print(f"\n  Missing Components ({len(report.completion_check.missing_components)}):")
        for component in report.completion_check.missing_components:
            print(f"    - {component}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
