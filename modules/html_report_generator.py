import os


def generate_html_report(results, html_report_path):
    """
    Generates an HTML report based on Axe-core accessibility results.

    Args:
    - results: The results dictionary from the Axe-core accessibility audit.
    - html_report_path: The file path where the HTML report should be saved.
    """
    # Define inline CSS for the report
    css_content = """
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            padding: 20px;
            background-color: #f4f4f4;
        }
        h1 {
            color: #2c3e50; /* Dark blue for main heading */
            border-bottom: 2px solid #2980b9; /* Blue underline */
            padding-bottom: 10px;
        }
        h2 {
            color: #2980b9; /* Bright blue for subheadings */
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background: #fff;
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        a {
            color: #e74c3c; /* Red for links */
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .violation-description {
            color: #8e44ad; /* Purple for violation descriptions */
            font-weight: bold;
        }
        .impact {
            color: #d35400; /* Orange for impact descriptions */
        }
    </style>
    """

    # Start writing the HTML report
    with open(html_report_path, 'w', encoding='utf-8') as html_file:
        # Write the basic HTML structure
        html_file.write("<!DOCTYPE html>")
        html_file.write("<html lang='en'>")
        html_file.write("<head>")
        html_file.write("<meta charset='UTF-8'>")
        html_file.write("<title>Accessibility Report</title>")

        # Write the CSS
        html_file.write(css_content)

        html_file.write("</head>")
        html_file.write("<body>")
        html_file.write("<h1>Accessibility Report</h1>")

        # Generate report content based on violations
        violations = results["violations"]
        if len(violations) == 0:
            html_file.write("<h2>No accessibility violations found!</h2>")
        else:
            html_file.write("<h2>Violations</h2><ul>")
            for violation in violations:
                html_file.write("<li>")
                html_file.write(f"<span class='violation-description'>{violation['description']}</span><br>")
                html_file.write(f"<span class='impact'>Impact: {violation['impact']}</span><br>")
                html_file.write(f"<a href='{violation['helpUrl']}'>Learn more</a><br>")
                html_file.write("<ul>")
                for node in violation["nodes"]:
                    html_file.write(f"<li>Element: {node['html']}</li>")
                    html_file.write(f"<li>Failure Summary: {node['failureSummary']}</li>")
                html_file.write("</ul></li>")
            html_file.write("</ul>")

        # Close the HTML structure
        html_file.write("</body></html>")

    print(f"Report generated at: {html_report_path}")
