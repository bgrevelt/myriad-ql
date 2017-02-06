//options {backtrack=true; memoize=true;}
/*
@parser::header
{
package org.uva.ak_bvdb.taxfree.raw;
}

@lexer::header
{
package org.uva.ak_bvdb.taxfree.raw;
*/

/** This grammar is an example illustrating the three kinds
 * of comments.
 */
grammar Grammar;
/* a multi-line
  comment
*/

/** This rule matches a declarator for my language */
decl : ID ; // match a variable name

ID : a=NameStartChar NameChar*
     {
     if ( Character.isUpperCase(getText().charAt(0)) ) setType(TOKEN_REF);
     else setType(RULE_REF);
     }
   ;

fragment
NameChar
  : NameStartChar
  | '0'..'9'
  | '_'
  | '\u00B7'
  | '\u0300'..'\u036F'
  | '\u203F'..'\u2040'
  ;
fragment
NameStartChar
  : 'A'..'Z' | 'a'..'z'
  | '\u00C0'..'\u00D6'
  | '\u00D8'..'\u00F6'
  | '\u00F8'..'\u02FF'
  | '\u0370'..'\u037D'
  | '\u037F'..'\u1FFF'
  | '\u200C'..'\u200D'
  | '\u2070'..'\u218F'
  | '\u2C00'..'\u2FEF'
  | '\u3001'..'\uD7FF'
  | '\uF900'..'\uFDCF'
  | '\uFDF0'..'\uFFFD'
  ;