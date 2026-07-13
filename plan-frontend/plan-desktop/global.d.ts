declare namespace JSX {
    interface IntrinsicElements {
        'css-doodle': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement> & {
            grid?: string | number;
            use?: string;
            seed?: string;
        };
    }
}