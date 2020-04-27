export const SET_DOCUMENT = 'setDocument';
export const SET_VARIABLES = 'setVariables';
export const SET_VARIABLE = 'setVariable';
export const REMOVE_VARIABLE = 'removeVariable';
// We differentiate between document template and template, as some
// actions might be executed from within a document context, thus
// modifying the document state itself.
export const SET_DOCUMENT_TEMPLATE = 'setDocumentTemplate';
