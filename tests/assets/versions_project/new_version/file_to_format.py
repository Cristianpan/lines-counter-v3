class ReportGenerator:
    """
        This line exceeds 80 characters and is intentionally written this way for testing purposes.
    """
    def __init__(self, report_title, author_name):
        self.report_title = report_title
        self.author_name = author_name

    def generate_header(self):
        header = f"Report Title: {self.report_title}\nAuthor: {self.author_name}\n" #comentario
        return header

    def generate_section(self, section_title: str = "title", section_content: str = "content") -> str:
        formatted_section = f"\n== {section_title} ==\n{section_content}\n"
        return formatted_section

    def generate_long_line_example(self):
        # This line exceeds 80 characters and is intentionally written this way for testing purposes.
        return "This is an example of a very long line that definitely goes beyond eighty characters."

    def summarize(self):
        # Another example of a long line that is here just to demonstrate the line length violation clearly.
        summary = "This summary is intentionally verbose and long enough to exceed the character limit per line."
        return summary


def create_sample_report():
    generator = ReportGenerator("Annual Financial Report", "Johnathan Alexander Maxwell")
    header = generator.generate_header()
    intro = generator.generate_section("Introduction", "This report presents a detailed overview of our annual financial performance, which includes data from multiple sources and takes into account various economic factors.")
    conclusion = generator.generate_section("Conclusion", "The data indicates that the company has achieved stable growth across all departments, with notable increases in revenue and operational efficiency.")
    summary = generator.summarize()

    full_report = header + intro + conclusion + "\nSummary:\n" + summary
    print(full_report)


if __name__ == "__main__":
    create_sample_report()
