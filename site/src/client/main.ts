// The client entry point: everything the page does after the build rendered it.
import { startCopy } from "./copy";
import { startViews } from "./views";

startViews();
startCopy();
