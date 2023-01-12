class Validator(object):
    """
    Validator is is the single entry point for validation.
    It chooses the configured validateType based on the validateTypeDesc parameter
    from the configuration section 'validators'.
    """

    @staticmethod
    def validate(value, validateDesc, context=None):
        """
        Validate the given value against the given validateType description.
        @param $value The value to validate
        @param $validateDesc A string in the form validateTypeA,validateTypeB:optionsB, where
            validateType is a key in the configuration section 'validators' and
            options is a JSON encoded object as used in the 'validate_type' definition
        @param $context An associative array describing the validation context which will be passed
            to the ValidateType::validate() method (optional)
        @return Boolean
        """

        # get validator list
        validators = []

        # split validateTypeDesc by commas and colons (separates validateType from options)
        validateDescParts = []
        re.findall('\{(?:[^{}]|(?R))+\}|[^{}:,\s]+', validateDesc, validateDescParts)
        # combine validateType and options again
        for validateDescPart in validateDescParts[0]:
            if re.match('^\{.*?\}$', validateDescPart):
                # options of preceding validator
                numValidators = len(validators)
                if numValidators > 0:
                    validators[numValidators-1] += ':'+validateDescPart
            else:
                validators.append(validateDescPart)

        # validate against each validator
        for validator in validators:
            validateTypeName, validateOptions = re.split('/:/', validator, 2)
            validateTypeName = validateTypeName or None
            validateOptions = validateOptions or None

            # get the validator that should be used for this value
            validatorInstance = Validator.getValidateType(validateTypeName)
            if validateOptions is not None:
                decodedOptions = json.loads(validateOptions)
                if decodedOptions is None:
                    raise ConfigurationException("No valid JSON format: "+validateOptions)
                validateOptions = decodedOptions
            if not validatorInstance.validate(value, validateOptions, context):
                return False

        # all validators passed
        return True

    @staticmethod
    def getValidateType(validateTypeName):
        """
        Get the ValidateType instance for the given name.
        @param $validateTypeName The validate type's name
        @return ValidateType instance
        """
        validatorTypes = ObjectFactory.getInstance('validators')
        if not validatorTypes[validateTypeName]:
            raise ConfigurationException("Configuration section 'Validators' does not contain a validator named: "+validateTypeName)
        return validatorTypes[validateTypeName]