import smtplib
import dns.resolver


def check_mx_records(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return [str(record.exchange) for record in records]
    except dns.resolver.NoAnswer:
        return None


def verify_email(email, sender_email='nraulik@yahoo.com', password=None):
    domain = email.split('@')[1]
    mx_records = check_mx_records(domain)

    if not mx_records:
        print(f"No MX records found for domain: {domain}")
        return False

    # Connect to the first MX server in the list
    mx_record = mx_records[0]

    try:
        # Try connecting with port 25 (unencrypted) or 587/465 (TLS encrypted)
        server = smtplib.SMTP(mx_record, 587, timeout=10)

        # Log in with SMTP AUTH
        if password:
            server.login(sender_email, password)

        server.set_debuglevel(1)  # Print the communication

        # Use dynamic domain for HELO
        server.helo(domain)

        # Use the sender_email parameter for MAIL FROM
        server.mail(sender_email)

        # Use the email passed to the function for RCPT TO
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            print("Email exists")
            return True
        else:
            print(f"Email verification failed: {message}")
            return False
    except Exception as e:
        print(f"Error connecting to SMTP server: {e}")
        return False


# Check Domain in Mail Xchange servers
domain = "re-connect.ro"
mx_records = check_mx_records(domain)

if mx_records:
    print(f"MX records found for {domain}: {mx_records}")
else:
    print(f"No MX records found for {domain}, domain may not accept emails.")


# Check SMTP & Individual mail response MX_Records
email = "contact@re-connect.ro"
verify_email(email)
