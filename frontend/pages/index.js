import React from "react";

import { makeStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";

import { Header, fPaths, getKey } from "../src";

const navLinks = [
  //{ title: `About`, path: fPaths.about },
  { title: `RFI Manager`, path: fPaths.rfiManager },
  { title: `Bid Tracker`, path: fPaths.platformer },
  //{ title: `Contact`, path: fPaths.contact },
];

const cards = [
  {
    imagePath: "/testImg.jpeg",
    imageTitle: "RFI Manager",
    cardTitle: "RFI Managerrrrr",
    desc: "A program that allows a company to track all of their rfis in one place.",
    gitHubLink: "#",
    linkToSite: fPaths.rfiManager,
  },

  {
    imagePath: "/testImg.jpeg",
    imageTitle: "Bid Tracker",
    cardTitle: "Bid Tracker",
    desc: "",
    gitHubLink: "#",
    linkToSite: fPaths.platformer,
  },
];

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  card: {
    height: "100%",
    display: "grid",
    flexDirection: "column",
  },
  media: {
    height: 140,
  },
}));

export default function Home() {
  const classes = useStyles();
  return (
    <>
      <Header links={navLinks} />
      <div className={classes.root}>
        <Grid container spacing={4}>
          {cards.map((card) => {
            return (
              <Grid key={getKey()} item xs={12} sm={6} md={6}>
                <Card key={getKey()} className={classes.card}>
                  <CardActionArea>
                    <CardMedia
                      className={classes.media}
                      image={card.imagePath}
                      title={card.imageTitle}
                    />
                    <CardContent>
                      <Typography gutterBottom variant="h5" component="h2">
                        {card.cardTitle}
                      </Typography>
                      <Typography
                        variant="body2"
                        color="textSecondary"
                        component="p"
                      >
                        {card.desc}
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                  <CardActions>
                    <Button href={card.gitHubLink} size="small" color="primary">
                      Github
                    </Button>
                    <Button href={card.linkToSite} size="small" color="primary">
                      Learn More
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            );
          })}
        </Grid>
      </div>
    </>
  );
}
