import React from "react";

import AppBar from "@material-ui/core/AppBar";
import Button from "@material-ui/core/Button";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";

import { getKey } from "../../utils";
import { Link } from "../nav";

type links = {
  path: string;
  title: string;
};

interface Props {
  links: Array<links>;
  title?: string;
}

const useStyles = makeStyles((theme) => ({
  appBar: {
    borderBottom: `1px solid ${theme.palette.divider}`,
  },
  toolbar: {
    flexWrap: "wrap",
  },
  toolbarTitle: {
    flexGrow: 1,
  },
  link: {
    margin: theme.spacing(1, 1.5),
  },
}));

export const Header: React.FC<Props> = ({ links, title }) => {
  const classes = useStyles();

  return (
    <>
      <AppBar
        position="static"
        color="default"
        elevation={0}
        className={classes.appBar}
      >
        <Toolbar className={classes.toolbar}>
          <Typography
            variant="h6"
            color="inherit"
            noWrap
            className={classes.toolbarTitle}
          >
            {title === undefined || title === null ? "Project Director" : title}
          </Typography>
          <nav>
            {links.map((l: links) => {
              return (
                <Link
                  key={getKey()}
                  color="textPrimary"
                  to={l.path}
                  className={classes.link}
                >
                  {l.title}
                </Link>
              );
            })}
          </nav>
          {/* <Button href="#" color="primary" variant="outlined" className={classes.link}>
                    Login
                </Button> */}
        </Toolbar>
      </AppBar>
    </>
  );
};
