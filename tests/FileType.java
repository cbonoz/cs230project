//duplicate example
package org.test.toolkit.file;

public interface FileType {

    public enum Image implements FileType {

        JPG;

        public String toString() {  //duplicated code
            return "." + super.toString().toLowerCase();
        };
    }

    public enum Office implements FileType {

        DOC;

        public String toString() {
            return "." + super.toString().toLowerCase();
        };
    }

    public enum PlainText implements FileType {

        TXT;

        public String toString() {  //duplicated code
            return "." + super.toString().toLowerCase();
        };
    }

}