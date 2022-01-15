import React, { useEffect } from "react";

import { useRouter } from "next/router";

import CssBaseline from "@material-ui/core/CssBaseline";
import { Theme, createStyles, makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import Paper from "@material-ui/core/Paper";

import { useAuthContext, fPaths, Header } from "../../src";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    paper: {
      marginTop: theme.spacing(8),
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
    },
    avatar: {
      margin: theme.spacing(1),
      backgroundColor: theme.palette.secondary.main,
    },
    form: {
      width: "100%",
      marginTop: theme.spacing(3),
    },
    submit: {
      margin: theme.spacing(3, 0, 2),
    },
  })
);

const navLinks = [{ title: `Home`, path: fPaths.home }];

interface Props {}

const WaitForEmailConfirm: React.FC<Props> = () => {
  /*
  This page is where the user goes after they submit an email. If the user successfully
  creates an account on the email-confirmation page they will be redirect from this page to 
  the pm home page.
  */
  const classes = useStyles();
  const router = useRouter();
  const { isAuthenticated } = useAuthContext();

  //check to see if the user followed the confirm email link sent by the backend
  //if they followed it and successfully created an account, so they are authenticated
  //send them to the pm home page.
  useEffect(() => {
    console.log("possibly rerouting user!!!!!!", isAuthenticated);
    if (isAuthenticated) router.push(fPaths.rfiManager);
  }, [isAuthenticated]);

  return (
    <>
      <Header links={navLinks} />
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper}>
          <Paper variant="outlined" className={classes.form}>
            <p>You should receive an email to confirm your email shortly.</p>
          </Paper>
        </div>
      </Container>
    </>
  );
};

export default WaitForEmailConfirm;
