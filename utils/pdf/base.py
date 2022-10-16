from xhtml2pdf import pisa  # import python module

# Define your data
source_html = "<html><body><b>bonjour bienfait</b></body></html>"
output_filename = "test.pdf"

# Utility function


def convert_html_to_pdf(source_html, output_filename):
    with open(output_filename, "w+b") as result_file:
        # convert HTML to PDF
        pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # return False on success and True on errors
    return pisa_status.err  # type: ignore


# Main program
if __name__ == "__main__":
    pisa.showLogging()
    convert_html_to_pdf(source_html, output_filename)
