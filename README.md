![Banner](banner.png)

# dm-data-format-consistency-enforcer
Ensures data within a column or field adheres to a consistent format (e.g., phone numbers, zip codes) by standardizing the format of the supplied value according to a defined pattern. - Focused on Tools designed to generate or mask sensitive data with realistic-looking but meaningless values

## What happens to a supplied value

When you supply a value, the tool reformats that value and keeps its content where the format allows it:

- `phone_number`: the supplied digits are kept and regrouped. A 10 digit number prints as `(AAA) BBB-CCCC`, and an 11 digit number starting with 1 prints with a `+1` prefix.
- `zip_code`: the supplied letters and digits are kept. A 9 digit code prints as `12345-6789`.
- `email`: a supplied value that is an email address is carried through unchanged.
- `ssn`: the supplied 9 digits are kept and printed as `AAA-BB-CCCC`.
- `credit_card_number`: the supplied digits (12 to 19 of them) are kept and regrouped in fours, separated by dashes.

Substitution cases: a supplied value that does not match the kind of data the named format holds cannot be reformatted without inventing content. For example, text that is not an email address supplied under `email`, or an SSN with other than 9 digits, is replaced with a freshly generated value in the named format, and the run logs that a substitute was returned. When no value is supplied at all, the tool generates values in the named format, as many as `--count` asks for.

## Install
`git clone https://github.com/ShadowGuardAI/dm-data-format-consistency-enforcer`

## Usage
`./dm-data-format-consistency-enforcer [params]`

## Parameters
- `-h`: Show help message and exit
- `format_type`: One of phone_number, zip_code, email, ssn, credit_card_number.
- `input_data`: The value to reformat (optional). See the section above for which formats preserve its content and when a generated substitute is returned instead.
- `--locale`: The locale to use (e.g., en_US, de_DE). Default is en_US.
- `--count`: The number of formatted values to generate when no input data is provided. Default is 1.

## License
Copyright (c) ShadowGuardAI
