export type VNodeType = string | Function;

export interface VNodeProps {
  [key: string]: any;
  children: VNode[];
}

export interface VNode {
  type: VNodeType;
  props: VNodeProps;
}

