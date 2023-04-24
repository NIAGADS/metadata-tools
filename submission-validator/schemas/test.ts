// config schema typescript
// To convert to JSON schema: typescript-json-schema schemas/config-schema.ts "*" --out <full_path_to_output_file> --required

// type ValidatorType = "warn_if_missing" | "age" | "regexp" | "units" | "depends_on" | "data_dictionary" | "list";
// type FieldDataType = "string" | "integer" | "clob" | "float" | "boolean";
    // type: ValidatorType;
/**
 * Validator specification
 * @additionalProperties false
 */
export interface FieldValidator {
    /**
     * type of validator
     */
    type: string;

    /**
     * options for the validator; a basic object
    */
   //options?: {[key: string]: string};     
   // value: string | string[];
}
