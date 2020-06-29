export const SET_DOCUMENT = 'setDocument';
export const SET_VARIABLES = 'setVariables';
export const SET_VARIABLE = 'setVariable';
export const ADD_VARIABLE = 'addVariable';
export const REMOVE_VARIABLE = 'removeVariable';
// We differentiate between document template and template, as some
// actions might be executed from within a document context, thus
// modifying the document state itself.
export const SET_TEMPLATE = 'setTemplate';
export const SET_STYLESHEET = 'setStylesheet';
export const SET_STYLESHEETS = 'setStylesheets';
export const SET_RESOURCE = 'setResource';
export const SET_RESOURCES = 'setResources';
export const REMOVE_RESOURCE = 'removeResource';
