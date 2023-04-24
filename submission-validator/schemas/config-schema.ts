// config schema typescript
// To convert to JSON schema: typescript-json-schema schemas/config-schema.ts "*" --out <full_path_to_output_file> --required

type ValidatorType = "warn_if_missing" | "age" | "regexp" | "units" | "depends_on" | "data_dictionary" | "list";
type FieldDataType = "string" | "integer" | "clob" | "float" | "boolean";

/**
 * Validator specification
 * @additionalProperties false
 */
export interface FieldValidator {
    /**
     * type of validator
     */
    type: ValidatorType;

    /**
     * options for the validator; a basic object
     * @additionalProperties false
     */
    options: {[key: string]: string};     
    values: string[];
}

/**
 * Metadata File Field Specification
 * @additionalProperties false
 */
export interface Field {
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

    type?: FieldDataType;

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
    validators?: FieldValidator[];
}


/**
 * Metadata File Validator Configuration
 * @additionalProperties false
 */

export interface MetadataFile {


    /**
     * name of the sheet
     * 
     * @TJS-type string
     */
    name: string;

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
    fields: Field[]

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