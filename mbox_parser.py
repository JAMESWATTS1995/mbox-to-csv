import mailbox
import unicodecsv as csv

# review https://www.oreilly.com/library/view/mining-the-social/9781449368180/ch06.html

# constants
export_file_name = "clean_mail.csv"

# get body of email
def get_contents(email):
    if email.is_multipart():
        body = ""
        parts = email.get_payload(decode=True)
        if parts is not None:
            for part in parts:
                if part.is_multipart():
                    for subpart in part.walk():
                        if subpart.get_content_type() == "text/html":
                            body += str(subpart)
                        elif subpart.get_content_type() == "text/plain":
                            body += str(subpart)
                else:
                    body += str(part)
        return body
    else:
        return email.get_payload()

if __name__ == "__main__":

    # get mbox file
    mbox_file = input("path to MBOX file: ")

    # create CSV file
    writer = csv.writer(open(export_file_name, "wb"), encoding='utf-8')

    # create header row
    writer.writerow(["date", "from", "to", "cc", "subject", "content"])

    # add rows based on mbox file
    for email in mailbox.mbox(mbox_file):
        contents = get_contents(email)
        writer.writerow([email["date"], email["from"], email["to"], email["cc"], email["subject"], contents])

    # print finish message
    print("generated CSV file called " + export_file_name)
