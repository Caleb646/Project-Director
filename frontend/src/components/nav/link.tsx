import React from "react";
import Link from "next/link";

interface Props extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  to: string;
  prefetch?: boolean;
}

export default React.forwardRef(
  ({ to, prefetch, ...props }: Props, ref: any) => {
    return (
      <Link href={to} prefetch={prefetch || true}>
        <a {...props} ref={ref} />
      </Link>
    );
  }
);
