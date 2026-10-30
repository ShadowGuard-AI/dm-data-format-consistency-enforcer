![Banner](banner.png)

# dm-data-format-consistency-enforcer
Ensures data within a column or field adheres to a consistent format (e.g., phone numbers, zip codes) by standardizing the format according to a defined pattern, even if the underlying data is masked. - Focused on Tools designed to generate or mask sensitive data with realistic-looking but meaningless values

## Install
`git clone https://github.com/ShadowGuardAI/dm-data-format-consistency-enforcer`

## Usage
`./dm-data-format-consistency-enforcer [params]`

## Parameters
- `-h`: Show help message and exit
- `--locale`: The locale to use (e.g., en_US, de_DE). Default is en_US.
- `--count`: The number of formatted values to generate when no input data is provided. Default is 1.

## License
Copyright (c) ShadowGuardAI
