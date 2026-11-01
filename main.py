import argparse
import logging
import re
import sys
from faker import Faker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataFormatEnforcer:
    """
    Enforces data format consistency within a column or field,
    even if the underlying data is masked.
    """

    def __init__(self, format_type, locale='en_US'):
        """
        Initializes the DataFormatEnforcer.

        Args:
            format_type (str): The type of format to enforce (e.g., 'phone_number', 'zip_code').
            locale (str): The locale to use for Faker (e.g., 'en_US', 'de_DE').
        """
        self.format_type = format_type
        self.fake = Faker(locale)
        self.formatter = self._get_formatter()  # Determines which function to use for formatting

    def _get_formatter(self):
        """
        Returns the appropriate Faker method based on the format type.
        """
        if self.format_type == 'phone_number':
            return self.fake.phone_number
        elif self.format_type == 'zip_code':
            return self.fake.postcode
        elif self.format_type == 'email':
            return self.fake.email
        elif self.format_type == 'ssn':
            return self.fake.ssn
        elif self.format_type == 'credit_card_number':
            return self.fake.credit_card_number
        else:
            logging.error(f"Unsupported format type: {self.format_type}")
            raise ValueError(f"Unsupported format type: {self.format_type}")

    def _reformat(self, data):
        """
        Reformats the supplied value, preserving its content.

        Returns the reformatted value, or None when the supplied value
        does not match the kind of data this format holds, in which case
        the caller falls back to generating a substitute value.
        """
        text = str(data).strip()
        if self.format_type == 'phone_number':
            digits = re.sub(r'\D', '', text)
            if len(digits) == 11 and digits.startswith('1'):
                return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
            if len(digits) == 10:
                return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
            if len(digits) == 7:
                return f"{digits[:3]}-{digits[3:]}"
            if len(digits) > 7:
                # Any other length over 7 digits is grouped in threes
                # with dashes. That shape is invented here rather than
                # taken from a numbering plan, so an 8 or 9 digit
                # number comes back in a format no phone system uses,
                # but with its digits intact and in order.
                prefix = "+" if text.startswith('+') else ""
                groups = [digits[i:i + 3] for i in range(0, len(digits), 3)]
                return prefix + "-".join(groups)
            return None
        elif self.format_type == 'zip_code':
            cleaned = re.sub(r'[^A-Za-z0-9]', '', text).upper()
            if not cleaned:
                return None
            if cleaned.isdigit() and len(cleaned) == 9:
                return f"{cleaned[:5]}-{cleaned[5:]}"
            return cleaned
        elif self.format_type == 'email':
            # An address that matches is returned exactly as given, so
            # for email the enforcement is only a shape test: nothing
            # is normalised, and an address that fails the test is not
            # repaired but replaced by a generated one in the caller.
            if re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", text):
                return text
            return None
        elif self.format_type == 'ssn':
            digits = re.sub(r'\D', '', text)
            if len(digits) == 9:
                return f"{digits[:3]}-{digits[3:5]}-{digits[5:]}"
            return None
        elif self.format_type == 'credit_card_number':
            digits = re.sub(r'\D', '', text)
            if 12 <= len(digits) <= 19:
                return "-".join(digits[i:i + 4] for i in range(0, len(digits), 4))
            return None
        return None

    def enforce_format(self, data):
        """
        Enforces the defined format on the input data.

        When data is supplied, its content is reformatted into the named
        format where the format allows it: digits in phone numbers, SSNs,
        and card numbers are regrouped, zip codes keep their characters,
        and an email address is carried through unchanged. A supplied
        value that does not match the kind of data the format holds
        cannot be reformatted without inventing content, so a generated
        substitute is returned instead. When no data is supplied, a
        generated value is returned.

        Args:
            data (str): The input data to format.

        Returns:
            str: The formatted data.  Returns None if formatting fails.
        """
        try:
            if data is not None:
                reformatted = self._reformat(data)
                if reformatted is not None:
                    return reformatted
                logging.info(
                    "Supplied value does not match the %s format kind; "
                    "returning a generated substitute value.", self.format_type)
            return self.formatter()
        except Exception as e:
            logging.error(f"Error enforcing format: {e}")
            return None


def setup_argparse():
    """
    Sets up the argparse command-line interface.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """
    parser = argparse.ArgumentParser(description="Enforces data format consistency. A supplied value is reformatted with its content preserved where the format allows it: phone_number, ssn, and credit_card_number regroup the supplied digits, zip_code keeps the supplied characters, and email carries a supplied email address through. A supplied value that does not match the format kind is replaced with a generated substitute. With no input value, a generated value is printed.")
    parser.add_argument("format_type", help="The type of format to enforce (e.g., phone_number, zip_code, email, ssn, credit_card_number)")
    parser.add_argument("input_data", nargs='?', default=None, help="The input data to format (optional). Its content is preserved by reformatting where the format allows it; a value that does not match the format kind is replaced with a generated substitute. If not provided, a single formatted value is generated.") #Input is now optional
    parser.add_argument("--locale", default="en_US", help="The locale to use (e.g., en_US, de_DE). Default is en_US.")
    parser.add_argument("--count", type=int, default=1, help="The number of formatted values to generate when no input data is provided. Default is 1.")

    return parser


def main():
    """
    Main function to parse arguments, enforce data format, and output the result.
    """
    try:
        parser = setup_argparse()
        args = parser.parse_args()

        # Input validation
        supported_formats = ["phone_number", "zip_code", "email", "ssn", "credit_card_number"]
        if args.format_type not in supported_formats:
            logging.error(f"Invalid format type: {args.format_type}. Supported types are: {supported_formats}")
            print(f"Error: Invalid format type. Supported types are: {supported_formats}") #output error for user, outside of log
            sys.exit(1)
        
        if args.count < 1 and args.input_data is None:
            logging.error("Count must be a positive integer when no input data is provided.")
            print("Error: Count must be a positive integer when no input data is provided.") #User facing error
            sys.exit(1)


        enforcer = DataFormatEnforcer(args.format_type, args.locale)

        if args.input_data:
            # Enforce format on the provided input data
            # --count plays no part on this branch: one value in, one
            # value out, however many were asked for.
            formatted_data = enforcer.enforce_format(args.input_data)
            if formatted_data:
                print(formatted_data)
            else:
                logging.error("Failed to format data.")
                print("Error: Failed to format data.") #User facing error
                sys.exit(1)
        else:
            # Generate a specified number of formatted values
            for _ in range(args.count):
                formatted_data = enforcer.enforce_format(None)
                if formatted_data:
                    print(formatted_data)
                else:
                    logging.error("Failed to generate formatted data.")
                    print("Error: Failed to generate formatted data.") #User facing error
                    sys.exit(1)

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}") #User facing error
        sys.exit(1)


if __name__ == "__main__":
    main()