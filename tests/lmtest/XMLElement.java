public class XMLElement {

    //when determining long method, we reason about the number of statements 
    // indepdent of the amount of white space in the program (by using an AST)
    //if counting keyword statement like while, for, if, etc: 81
    // excluding else, if, etc. : length 53
    protected void scanElement(XMLElement elt)
            throws IOException
        {
            StringBuffer buf = new StringBuffer();
            this.scanIdentifier(buf);
            String name = buf.toString();
            elt.setName(name);
            char ch = this.scanWhitespace();
            while ((ch != '>') && (ch != '/')) {
                buf.setLength(0);
                this.unreadChar(ch);
                this.scanIdentifier(buf);
                String key = buf.toString();
                ch = this.scanWhitespace();
                if (ch != '=') {
                    throw this.expectedInput("=");
                }
                this.unreadChar(this.scanWhitespace());
                buf.setLength(0);
                this.scanString(buf);
                elt.setAttribute(key, buf);
                ch = this.scanWhitespace();
            }
            if (ch == '/') {
                ch = this.readChar();
                if (ch != '>') {
                    throw this.expectedInput(">");
                }
                return;
            }
            buf.setLength(0);
            ch = this.scanWhitespace(buf);
            if (ch != '<') {
                this.unreadChar(ch);
                this.scanPCData(buf);
            } else {
                for (;;) {
                    ch = this.readChar();
                    if (ch == '!') {
                        if (this.checkCDATA(buf)) {
                            this.scanPCData(buf);
                            break;
                        } else {
                            ch = this.scanWhitespace(buf);
                            if (ch != '<') {
                                this.unreadChar(ch);
                                this.scanPCData(buf);
                                break;
                            }
                        }
                    } else {
                        if ((ch != '/') || this.ignoreWhitespace) {
                            buf.setLength(0);
                        }
                        if (ch == '/') {
                            this.unreadChar(ch);
                        }
                        break;
                    }
                }
            }
            if (buf.length() == 0) {
                while (ch != '/') {
                    if (ch == '!') {
                        ch = this.readChar();
                        if (ch != '-') {
                            throw this.expectedInput("Comment or Element");
                        }
                        ch = this.readChar();
                        if (ch != '-') {
                            throw this.expectedInput("Comment or Element");
                        }
                        this.skipComment();
                    } else {
                        this.unreadChar(ch);
                        XMLElement child = this.createElement();
                        this.scanElement(child);
                        elt.addChild(child);
                    }
                    ch = this.scanWhitespace();
                    if (ch != '<') {
                        throw this.expectedInput("<");
                    }
                    ch = this.readChar();
                }
                this.unreadChar(ch);
            } else {
                if (this.ignoreWhitespace) {
                    elt.setContent(buf.toString().trim());
                } else {
                    elt.setContent(buf.toString());
                }
            }
            ch = this.readChar();
            if (ch != '/') {
                throw this.expectedInput("/");
            }
            this.unreadChar(this.scanWhitespace());
            if (! this.checkLiteral(name)) {
                throw this.expectedInput(name);
            }
            if (this.scanWhitespace() != '>') {
                throw this.expectedInput(">");
            }

        }
    }