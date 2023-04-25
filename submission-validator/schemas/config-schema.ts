// config schema typescript
// To convert to JSON schema: 
// typescript-json-schema schemas/config-schema.ts "sheet" --out schemas/config-schema.json --required --topRef --titles --noExtraProps

type validator_type = "warn_if_missing" | "age" | "regexp" | "units" | "depends_on" | "data_dictionary" | "list" | "delimiter";
type field_data_type = "string" | "integer" | "clob" | "float" | "boolean";
type test_type = "null" | "match";

/**
 * Validator specification
 * @additionalProperties false
 */
export interface field_validator {
    /**
     * type of validator
     */
    type: validator_type;

    /**
     * options for the validator; a basic object
     * @additionalProperties false
     */
    options?: {[key: string]: string };     

    /**
     * 
     * validator value (may be a list of items or a test)
     * @uniqueItems true
     * @minItems 1
     */
    value?: string | string[];
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
    validator?: field_validator[];
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
    fields: field[]

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