class ValidateType(object):
    """
    ValidateType defines the interface for all validator classes.
    """

    def validate(self, value, options=None, context=None):
        """
        Validate a given value. The options format is type specific.
        @param value The value to validate
        @param options Optional implementation specific options passed as an associative array
        @param context An associative array describing the validation context (optional)
        @return Boolean
        """
        pass

class RegExp(ValidateType):
  """
  RegExp validates against the given regular expression.

  Configuration example:
  // integer or empty
  regexp:{"pattern":"/^[0-9]*$/"}
  """

  def validate(self, value, options=None, context=None):
    if not 'pattern' in options:
      raise ConfigurationException("No 'pattern' given in regexp options: ".json_encode($options))
    return re.match(options['pattern'], value)
    
class Required(ValidateType):
  """
  Required checks if the value is not empty.

  Configuration examples:
  @code
  required
  @endcode
  """

  def validate(self, value, options=None, context=None):
    return isinstance(value, list) and len(value) > 0 or len(value) > 0

class Unique(ValidateType):

    def validate(self, value, options=None, context=None):
        if len(value) == 0:
            return True

        # get type and value from context, if not set
        if not 'type' in options and 'entity' in context:
            options['type'] = context['entity'].get_type()
        if not 'value' in options and 'value' in context:
            options['value'] = context['value']

        # validate options
        if not 'type' in options:
            raise ConfigurationException("No 'type' given in unique options: "+json.dumps(options))
        if not 'value' in options:
            raise ConfigurationException("No 'value' given in unique options: "+json.dumps(options))

        type = options['type']
        attribute = options['value']
        query = ObjectQuery(type)
        itemTpl = query.get_object_template(type)
        # force set to skip validation
        itemTpl.set_value(attribute, Criteria.as_value("=", value), True)
        itemOidList = query.execute(False)
        # exclude context entity
        if 'entity' in context:
            oid = context['entity'].get_oid()
            itemOidList = list(filter(lambda itemOid: itemOid != oid, itemOidList))

        # value already exists
        if len(itemOidList) > 0:
            return False
        return True

class Date(ValidateType):
    DEFAULT_FORMAT = 'Y-m-d'

    def validate(self, value, options=None, context=None):
        format = options['format'] if options and 'format' in options else self.DEFAULT_FORMAT
        return len(value) == 0 or (datetime.strptime(value, format) != False)