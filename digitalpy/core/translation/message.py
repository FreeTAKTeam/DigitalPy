#######################################################
# 
# message.php
# Python implementation of the Interface Message
# Generated by Enterprise Architect
# Created on:      29-Aug-2022 4:56:38 PM
# Original author: ingo herwig <ingo@wemove.com>
# 
#######################################################


from typing import Any
from abc import ABC, abstractmethod

class Message:
    """Message is used to get localized messages to be used in the user interface.
      @note The language of a message is determined in one of 3 ways (in this
    order): -# use the value of the lang parameter passed to Message::getText() -#
    use the value of language from the Message configuration section -# use the
    value of the global Anyiable $_SERVER['HTTP_ACCEPT_LANGUAGE']
    """
    
    @abstractmethod
    def get_all(self, lang : Any = '') -> Any:
        """_get a list of all localized strings.
           @param $lang _the language (optional, default: '')
           @return _an array of localized strings
        """

    @abstractmethod
    def get_text(self, message : Any, parameters : Any = None, lang : Any = '') -> Any:
        """_get a localized string.
           @note _it is not recommended to use this method with concatenated strings
        because this restricts the positions of words in translations. E.g. '_she was
        born in %0% on %1%' translates to the german sentence '_sie wurde am %1% in %0%
        geboren' with the Anyiables flipped.
           @note _implementations must return the original message, if no translation is
        found, or the translation string is empty.
           @param $message _the message to translate (%0%, %1%, ... will be replaced by
        given parameters).
           @param $parameters _an array of values for parameter substitution in the
        message.
           @param $lang _the language (optional, default: '')
           @return _the localized string
        """