# 📝 TunnelKeys (Python Keylogger Script) [![GitHub stars](https://img.shields.io/github/stars/PetrisGR/TunnelKeys.svg)](https://github.com/PetrisGR/TunnelKeys/stargazers) [![GitHub license](https://img.shields.io/github/license/PetrisGR/TunnelKeys.svg)](https://github.com/PetrisGR/TunnelKeys/blob/master/LICENSE)

"TunnelKeys" is a Python keylogger tool. It transmits the keys pressed via DNS tunneling using Base32 encoding.

**Note**: This tool does not provide a DNS listener. To capture, decode, and analyze keylogs transmitted via DNS tunneling, you will need to set up your own DNS server and listener to handle the incoming queries.

## Features

- **Base32 (DNS-Friendly) Encoded Data**: Transmits data using base32 encoding, ensuring compatibility with DNS subdomain constraints.
- **DNS Tunneling**: Leverages DNS tunneling to send chunks of captured keys.
- **Fully Configurable**: Allows you to configure DNS server settings, keypress handling, and encoding options for flexible use.

## Installation

1. Download the ZIP file or Clone the repository
2. Install dependencies via `pip install -r requirements.txt`
3. Set configurable values at the top of the script `tunnelkeys.py`
3. Run `tunnelkeys.py`

## Contributing

Contributions are welcome! Please submit a pull request if you have any ideas, suggestions, or improvements. For significant changes, please open an issue to discuss the proposed changes.

## Support

If you encounter any issues or have any questions or suggestions, please feel free to [open an issue](https://github.com/PetrisGR/TunnelKeys/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/PetrisGR/TunnelKeys/LICENSE) file for details.
