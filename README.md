# COMSW115-ScriptLite

Team Members: Puja Singla (ps3467), Ria Luo (xl3466)

# Installation Requirements

# Description of the Scanner

### Cursor
The cursor keeps track of the current position in the input program string. 
It increments as characters are processed.

### Tokens and Errors
- **Tokens**: A list that stores recognized tokens as tuples of (token type, token value).
- **Errors**: A list that records any lexical errors encountered during scanning.

## States and Transitions
The scanner transitions between different states based on the character being 
analyzed. The main states can be summarized as follows:

### State Transitions

#### Whitespace State
- **Transition**: If the character is whitespace, the scanner simply advances 
the cursor to skip over it.

#### Identifier/Keyword State
- **Transition**: If the character is alphabetic or an underscore, it indicates 
the beginning of an identifier or keyword.
  - The scanner enters a loop to collect all contiguous alphanumeric characters 
  or underscores, creating a lexeme.
  - After the loop, it checks if the lexeme is a keyword (by checking against the keywords set) 
  and adds the appropriate token (either `KEYWORD` or `IDENTIFIER`).

#### String State
- **Transition**: If the character is a double quote (`"`), the scanner 
recognizes the start of a string literal.
  - It advances the cursor and enters a loop until it finds the closing quote, 
  collecting characters for the string.
  - If it reaches the end of the line without finding the closing quote, 
  it records a lexical error for an unclosed string.

#### Separator State
- **Transition**: If the character is found in the separators string, 
it recognizes it as a separator and adds it as a `SEPARATOR` token.

#### Operator State
- **Transition**: If the character is found in the operators string, it 
recognizes it as an operator and adds it as an `OPERATOR` token.

#### Error State
- **Transition**: If the character does not match any of the above criteria, it’s 
considered an invalid character. The scanner records an error and advances the cursor.

### Error Handling
The scanner catches two main types of errors: invalid characters that do not 
conform to any recognized token types and unclosed string literals. When an 
invalid character is encountered, it logs a lexical error message indicating 
the character's position and type, allowing the scanner to continue processing 
the remainder of the input without interruption. For unclosed strings, the scanner
detects when a string literal begins with a double quote but lacks a corresponding
closing quote by the end of the line, recording this as an error as well. 
In both cases, the scanner advances the cursor to the next character after 
logging the error, ensuring that it can continue scanning the input rather than 
halting on encountering an error.
