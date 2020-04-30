export const VARIABLE = 'variable';
export const DOCUMENT = 'document';
export const TEMPLATE = 'template';
export const STYLESHEET = 'stylesheet';

export function variable(action) {
  return VARIABLE + '/' + action;
}

export function document(action) {
  return DOCUMENT + '/' + action;
}

export function template(action) {
  return TEMPLATE + '/' + action;
}

export function stylesheet(action) {
  return STYLESHEET + '/' + action;
}
