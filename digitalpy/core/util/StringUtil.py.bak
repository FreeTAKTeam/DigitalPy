
import re
import random
import string
import uuid
from html import unescape
from functools import reduce

class StringUtil:
    @staticmethod
def get_dump(variable, strlen=100, width=25, depth=10, i=0, objects=[]):
    search = ["\0", "\a", "\b", "\f", "\n", "\r", "\t", "\v"]
    replace = ['\0', '\a', '\b', '\f', '\n', '\r', '\t', '\v']

    string = ''

    var_type = type(variable)
    if var_type == bool:
        string += 'true' if variable else 'false'
    elif var_type in [int, float]:
        string += str(variable)
    elif var_type == type(None):
        string += 'null'
    elif var_type == str:
        len_ = len(variable)
        variable = variable[:strlen]
        variable = variable.replace(search, replace)
        if len_ < strlen:
            string += '"{}"'.format(variable)
        else:
            string += 'string({}): "{}"...'.format(len_, variable)
    elif var_type == list:
        len_ = len(variable)
        if i == depth:
            string += 'array({}) {{...}}'.format(len_)
        elif len_ == 0:
            string += 'array(0) {{}}'
        else:
            keys = list(range(len_))
            spaces = ' ' * (i*2)
            string += "array({})\n{}{{".format(len_, spaces)
            count = 0
            for key in keys:
                if count == width:
                    string += "\n{}  ...".format(spaces)
                    break
                string += "\n{}  [{}] => ".format(spaces, key)
                string += get_dump(variable[key], strlen, width, depth, i+1, objects)
                count += 1
            string += "\n{}}}".format(spaces)
    elif var_type == dict:
        len_ = len(variable)
        if i == depth:
            string += 'array({}) {{...}}'.format(len_)
        elif len_ == 0:
            string += 'array(0) {{}}'
        else:
            keys = list(variable.keys())
            spaces = ' ' * (i*2)
            string += "array({})\n{}{{".format(len_, spaces)
            count = 0
            for key in keys:
                if count == width:
                    string += "\n{}  ...".format(spaces)
                    break
                string += "\n{}  [{}] => ".format(spaces, key)
                string += get_dump(variable[key], strlen, width, depth, i+1, objects)
                count += 1
            string += "\n{}}}".format(spaces)
    elif var_type == object:
        id_ = objects.index(variable)
        if id_ != -1:
            string += '{}#{} {{...}}'.format(variable.__class__.__name__, id_+1)
	else {
          $id = array_push($objects, $variable);
          $array = (array)$variable;
          $spaces = str_repeat(' ', $i*2);
          $string .= get_class($variable)."#$id\n".$spaces.'{';
          $properties = array_keys($array);
          foreach ($properties as $property) {
            $name = str_replace("\0", ':', trim($property));
            $string .= "\n".$spaces."  [$name] => ";
            $string .= self::getDump($array[$property], $strlen, $width, $depth, $i+1, $objects);
          }
          $string .= "\n".$spaces.'}';
        }
        break;
    }

    if ($i > 0) {
      return $string;
    }

    $backtrace = debug_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS);
        do {
          $caller = array_shift($backtrace);
        } while ($caller && !isset($caller['file']));
        if ($caller) {
          $string = $caller['file'].':'.$caller['line']."\n".$string;
        }

        return $string;
      }
    }
import html

"""
   * Truncate a string up to a number of characters while preserving whole words and HTML tags.
   * Based on https://stackoverflow.com/questions/16583676/shorten-text-without-splitting-words-or-breaking-html-tags#answer-16584383
   * @param $text String to truncate.
   * @param $length Length of returned string (optional, default: 100)
   * @param $suffix Ending to be appended to the trimmed string (optional, default: …)
   * @param $exact Boolean whether to allow to cut inside a word or not (optional, default: false)
   * @return String
 """

def crop_string(text: str, length: int=100, suffix: str='…', exact: bool=False) -> str:
    if len(text) <= length:
        return text

    is_html = strip_tags(text) != text

    from lxml.html.soupparser import fromstring
    dom = fromstring(html.escape(text).encode('utf-8'))

    reached_limit = False
    total_len = 0
    to_remove = []
    def walk(node):
        nonlocal reached_limit, total_len, to_remove
        if reached_limit:
            to_remove.append(node)
        else:
            if node.text:
                total_len += node_len = len(node.text)
                if total_len > length:
                    space_pos = node.text.rfind(' ', 0, node_len-(total_len-length)-1)
                    node.text = node.text[:space_pos if not exact else node_len-(total_len-length)]
                    node.text += node.text and suffix or ''
                    reached_limit = True
            for child in node:
                walk(child)
        return to_remove

    to_remove = walk(dom)
    for child in to_remove:
        child.getparent().remove(child)

    result = html.unescape(dom.text_content())
    return result if is_html else html.unescape(strip_tags(result))


 """
   * Create an excerpt from the given text around the given phrase
   * code based on: http://stackoverflow.com/questions/1292121/how-to-generate-the-snippet-like-generated-by-google-with-php-and-mysql
   * @param $string
   * @param $phrase
   * @param $radius
  """
  
def excerpt(string, phrase, radius=100):
    if radius > len(string):
        return string

    phrase_len = len(phrase)
    if radius < phrase_len:
        radius = phrase_len

    pos = string.lower().find(phrase.lower())

    start_pos = 0
    if pos > radius:
        start_pos = pos - radius

    text_len = len(string)

    end_pos = pos + phrase_len + radius
    if end_pos >= text_len:
        end_pos = text_len

    # make sure to cut at spaces
    first_space_pos = string.find(" ", start_pos)
    last_space_pos = string.rfind(" ", -(text_len - end_pos))

    excerpt1 = string[first_space_pos:last_space_pos]

    # remove open tags
    excerpt = re.sub(r'^[^<]*?>|<[^>]*?$', '', excerpt1)
    return excerpt
    

"""
   * Extraxt urls from a string.
   * @param $string The string to search in
   * @return An array with urls
   * @note This method searches for occurences of <a..href="xxx"..>, <img..src="xxx"..>, <video..src="xxx"..>,
   * <audio..src="xxx"..>, <input..src="xxx"..>, <form..action="xxx"..>, <link..href="xxx"..>, <script..src="xxx"..>
   * and extracts xxx.
"""

def get_urls(string):
    links = re.findall(r"<a[^>]+href=\"([^\">]+)", string)
    for i, link in enumerate(links):
        popups = re.findall(r"javascript:.*window.open[(]*'([^']+)", link)
        if popups:
            links[i] = popups[0]
    links = [link for link in links if not link.startswith("mailto:")]
    images = re.findall(r"<img[^>]+src=\"([^\">]+)", string)
    videos = re.findall(r"<video[^>]+src=\"([^\">]+)", string)
    audios = re.findall(r"<audio[^>]+src=\"([^\">]+)", string)
    buttons = re.findall(r"<input[^>]+src=\"([^\">]+)", string)
    actions = re.findall(r"<form[^>]+action=\"([^\">]+)", string)
    css = re.findall(r"<link[^>]+href=\"([^\">]+)", string)
    scripts = re.findall(r"<script[^>]+src=\"([^\">]+)", string)
    return links + images + videos + audios + buttons + actions + css + scripts

"""
   * Split a quoted string
   * code from: http://php3.de/manual/de/function.split.php
   * @code
   * $string = '"hello, world", "say \"hello\"", 123, unquotedtext';
   * $result = quotsplit($string);
   *
   * // results in:
   * // ['hello, world'] [say "hello"] [123] [unquotedtext]
   *
   * @endcode
   *
   * @param $string The string to split
   * @return An array of strings
"""
    def quotesplit(string):
        r = []
        p = 0
        l = len(string)
        while p < l:
            while p < l and string[p] in " \r\t\n":
                p += 1
            if string[p] == '"':
                p += 1
                q = p
                while p < l and string[p] != '"':
                    if string[p] == '\\':
                        p += 2
                        continue
                    p += 1
                r.append(stripslashes(string[q:p]))
                p += 1
                while p < l and string[p] in " \r\t\n":
                    p += 1
                p += 1
            elif string[p] == "'":
                p += 1
                q = p
                while p < l and string[p] != "'":
                    if string[p] == '\\':
                        p += 2
                        continue
                    p += 1
                r.append(stripslashes(string[q:p]))
                p += 1
                while p < l and string[p] in " \r\t\n":
                    p += 1
                p += 1
            else:
                q = p
                while p < l and string[p] not in ",;":
                    p += 1
                r.append(stripslashes(string[q:p].strip()))
                while p < l and string[p] in " \r\t\n":
                    p += 1
                p += 1
        return r
"""
   * Split string preserving quoted strings
   * code based on: http://www.php.net/manual/en/function.explode.php#94024
   * @param $string String to split
   * @param $delim Regexp to use in preg_split
   * @param $quoteChr Quote character
   * @param $preserve Boolean whether to preserve the quote character or not
   * @return Array
  """
     def split_quoted(string, delim='/ /', quote_chr='"', preserve=False):
        res_arr = []
        n = 0
        exp_enc_arr = string.split(quote_chr)
        for enc_item in exp_enc_arr:
            if n % 2:
                res_arr[-1] += (quote_chr if preserve else '') + enc_item + (quote_chr if preserve else '')
            else:
                exp_del_arr = re.split(delim, enc_item)
                res_arr[-1] += exp_del_arr.pop(0)
                res_arr += exp_del_arr
            n += 1
        return res_arr
  """
   * Convert a string in underscore notation to camel case notation.
   * Code from http://snipt.net/hongster/underscore-to-camelcase/
   * @param $string The string to convert
   * @param $firstLowerCase Boolean whether the first character should be lowercase or not (default: _false_)
   * @return The converted string
  """
   def underScoreToCamelCase(string, firstLowerCase=False):
    if isinstance(string, str):
        str = string.replace(' ', '').title().replace('_', ' ')
        if firstLowerCase:
            str[0] = str[0].lower()
        return str
    else:
        return ''
 """
   * Escape characters of a string for use in a regular expression
   * Code from http://php.net/manual/de/function.preg-replace.php
   * @param $string The string
   * @return The escaped string
  """
  def escape_for_regex(string: str) -> str:
    patterns = ['/\\//', '/\\^/', '/\\./', '/\\$/', '/\\|/', '/\\(/', '/\\)/', '/\\[/', '/\\]/', '/\\*/', '/\\+/', '/\\?/', '/\\{/', '/\\}/']
    replace = ['\\\\/', '\\\\^', '\\\\.', '\\\\$', '\\\\|', '\\\\(', '\\\\)', '\\\\[', '\\\\]', '\\\\*', '\\\\+', '\\\\?', '\\\\{', '\\\\}']

    return re.sub(patterns, replace, string)

"""
   * Remove a trailing comma, if existing.
   * @param $string The string to crop
   * @return The string
"""
    def remove_trailing_comma(string: str) -> str:
        return re.sub(r', ?$', '', string)

"""
   * Get the boolean value of a string
   * @param $string
   * @return Boolean or the string, if it does not represent a boolean.
 """

    def get_boolean(string: str) -> Union[bool, str]:
        val = filter(lambda x: x is not None, [filter(string, bool, flags=FILTER_NULL_ON_FAILURE)])
        if not val:
            return string
        return val[0]
"""
   * Converts all accent characters to ASCII characters.

   * @param $string Text that might have accent characters
   * @return string Filtered string with replaced "nice" characters.
 """
 def slug(string):
    search = ['Ä', 'Ö', 'Ü', 'ä', 'ö', 'ü', 'ß']
    replace = ['AE', 'OE', 'UE', 'ae', 'oe', 'ue', 'ss']
    string = string.replace(search, replace)
    return string.lower().strip(re.sub(r'[^0-9a-z]+', '-', html.unescape(re.sub(r'&([a-z]{1,2})(?:acute|cedil|circ|grave|lig|orn|ring|slash|th|tilde|uml);', '$1', html.escape(string)))))
 
"""
   * Generate a v4 UUID
   * Code from https://stackoverflow.com/questions/2040240/php-function-to-generate-v4-uuid#15875555
   * @return string
"""
def guidv4():
    data = uuid.uuid4().bytes
    data[6] = (data[6] & 0x0f) | 0x40
    data[8] = (data[8] & 0x3f) | 0x80
    return '-'.join(['{:x}'.format(b) for b in data])
