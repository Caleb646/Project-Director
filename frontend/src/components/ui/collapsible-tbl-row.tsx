import React from "react";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  makeStyles,
  Box,
  Collapse,
  IconButton,
} from "@material-ui/core";

import KeyboardArrowDownIcon from "@material-ui/icons/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@material-ui/icons/KeyboardArrowUp";

import { getKey } from "../../utils";

const useRowStyles = makeStyles({
  root: {
    "& > *": {
      borderBottom: "unset",
    },
  },
});

interface RowProps {
  mainRow: Array<string | number | any>;
  subColumn: Array<string>;
  subRow: Array<string | number>;
}

export const CollapsibleTblRow: React.FC<RowProps> = ({
  mainRow,
  subColumn,
  subRow,
}) => {
  /*
   */
  const [open, setOpen] = React.useState(false);
  const classes = useRowStyles();
  return (
    <React.Fragment key={getKey()}>
      <TableRow key={getKey()} className={classes.root}>
        <TableCell key={getKey()}>
          <IconButton
            key={getKey()}
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? (
              <KeyboardArrowUpIcon key={getKey()} />
            ) : (
              <KeyboardArrowDownIcon key={getKey()} />
            )}
          </IconButton>
        </TableCell>

        {mainRow.map((value) => {
          return (
            <TableCell key={getKey()} component="th" scope="row">
              {value}
            </TableCell>
          );
        })}
      </TableRow>
      <TableRow key={getKey()}>
        <TableCell
          key={getKey()}
          style={{ paddingBottom: 0, paddingTop: 0 }}
          colSpan={6}
        >
          <Collapse key={getKey()} in={open} timeout="auto" unmountOnExit>
            <Box key={getKey()} margin={1}>
              {/* <Typography variant="h6" gutterBottom component="div">
                  Details
                </Typography> */}
              <Table key={getKey()} size="small" aria-label="purchases">
                <TableHead key={getKey()}>
                  <TableRow key={getKey()}>
                    {subColumn.map((label) => (
                      <TableCell>{label}</TableCell>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody key={getKey()}>
                  <TableRow key={getKey()}>
                    {subRow.map((value) => (
                      <TableCell key={getKey()} scope="row">
                        {value}
                      </TableCell>
                    ))}
                  </TableRow>
                </TableBody>
              </Table>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </React.Fragment>
  );
};

// {/* {subRow.map((value) => {
//                     return (
//                       <TableRow key={getKey()}>
//                         {value.map((v) => {
//                           return (
//                             <TableCell key={getKey()} scope="row">
//                               {v}
//                             </TableCell>
//                           );
//                         })}
//                       </TableRow>
//                     );
//                   })} */}
