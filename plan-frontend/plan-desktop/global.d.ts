import * as React from 'react';

declare module 'css-doodle';

declare global {
    namespace JSX {
        interface IntrinsicElements {
            'css-doodle': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement> & {
                children?: string;
                grid?: string | number;
                use?: string;
                seed?: string;
            };
        }
    }
}

export {}