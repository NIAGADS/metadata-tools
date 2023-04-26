// config schema typescript
// To convert to JSON schema:
// typescript-json-schema schemas/config-schema.ts "sheet" --out schemas/config-schema.json --required --topRef --titles --noExtraProps

type validator_type =
  | "warn_if_missing"
  | "age"
  | "regexp"
  | "units"
  | "test" // use when one field depends on the values in or existence of another field (same or different sheet)
  | "data_dictionary"
  | "list"
  | "delimiter"
  ;

type field_data_type = "string" | "integer" | "clob" | "float" | "boolean";

type pattern_type =
  | "email"
  | "publication" // DOI or pubmed
  | "URL"
  | "custom"; // supply custom pattern in the validator `value` field

type test_type = "value_exists" // (test) all values in the dependent field must exist in the independent field
  | "value_matches" // (test) a value in the independent field matches the test value
  | "all_fields_exist" // (test) require all fields in the set to be present
  | "any_fields_exist" // (test) require at least one field in the set to be present
  ; 
  

/**
 * Details about a depends_on (test-involving) validation
 * @additionalProperties false
 */

export interface test {
  /**
   * the type of the test
   */
  type: test_type;

  /**
   * field value(s) on which dependency is conditioned; Y/N should be specified as boolean
   */
  value?: string | number | boolean | string[];

  /**
   * sheet name if not same as field being validated
   * @TJS-type string
   */
  sheet?: string;

  /**
   * the field(s) on which the validation is dependent; assumes same sheet if `sheet` is not supplied
   *
   */
  field: string | string[];

  /**
   * flag indicating whether a warning instead of an error should be provided if the test fails
   * 
   * @TJS-type boolean
   * @default false
   */
  warn_if_fail?: boolean;
}

/**
 * Validator options
 * @additionalProps false
 */

export interface validator_options {
  /**
   * if type of validation is a test, provide the details
   */
  test?: test;

  /**
   * regexp pattern type; for custom pattern specifiy `custom` and then provide
   * the actual pattern in the "other"
   */
  pattern?: pattern_type;

   /**
   * allow free text; for data dictionary validation
   *
   * @TJS-type boolean
   * @default false
   */
  allow_user_terms?: boolean;

  /**
   * catch all to allow additional comments or qualifiersoptions for now, but still allow schema validation by not allowing additionalProperties
   *
   * @TJS-type string
   */
  comment?: string;
}

/**
 * Validator specification; validators can be provided for fields or sheets
 * @additionalProperties false
 */
export interface validator {
  /**
   * type of validator
   */
  type: validator_type;

  /**
   * options for the validator
   *
   * @additionalProperties false
   */
  options?: validator_options;

  /**
   *
   * validator value (may be a list of items or a test)
   * @uniqueItems true
   * @minItems 1
   */
  value?: string | string[];

  /**
   * message if validation fails or warning conditions are met
   * @TJS-type string
   */
    message?: string;
}

/**
 * Metadata File Field Specification
 * @additionalProperties false
 */
export interface field {
  /**
   * name of metadata field
   *
   * @TJS-type string
   */
  name: string;

  /**
   * data type of the field;
   *
   * @TJS-type string
   * @default string
   */

  type?: field_data_type;

  /**
   * flag indicating whether the field is required
   *
   * @TJS-type boolean
   * @default false
   */
  required?: boolean;

  /**
   * list of field validators
   */
  validator?: validator[];
}

/**
 * Metadata File (Sheet) Validator Configuration
 * @additionalProperties false
 */

export interface sheet {
  /**
   * name of the sheet
   *
   * @TJS-type string
   */
  sheet_name?: string;

  /**
   * flag indicating whether user-defined fields are allowed
   * @TJS-type boolean
   * @default false
   */
  allow_user_fields?: boolean;

  /**
   * list of expected fields in the sheet
   *
   * @uniqueItems true
   * @minItems 1
   */
  fields: field[];

  /**
   * to support inheritence; parent sheet type (e.g., `rnaseq_assay` extends `sequencing_assay`)
   *
   * @TJS-type string
   */
  extends?: string;

  /**
   * to support inheritence; any fields from the parent that should be omitted (ignored)
   *
   * @uniqueItems true
   * @minItems 0
   */
  omit_fields?: string[];
}
