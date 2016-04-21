class ImageValidator
{
    public function validate($value, Constraint $constraint)
    {
        if (null === $value || '' === $value) {
            return;
        }

        if (null === $constraint->minWidth && null === $constraint->maxWidth) {
            return;
        }

        $size = @getimagesize($value);
        if (empty($size) || ($size[0] === 0) || ($size[1] === 0)) {
            $this->context->addViolation($constraint->sizeNotDetectedMessage);

            return;
        }

        $width  = $size[0];
        $height = $size[1];

        if ($constraint->minWidth) {
            if (!ctype_digit((string) $constraint->minWidth)) {
                throw new ConstraintDefinitionException(sprintf('"%s" is not a valid minimum width', $constraint->minWidth));
            }

            if ($width < $constraint->minWidth) {
                $this->context->addViolation($constraint->minWidthMessage, array(
                    '{{ width }}'    => $width,
                    '{{ min_width }}' => $constraint->minWidth
                ));

                return;
            }
        }

        if ($constraint->maxWidth) {
            if (!ctype_digit((string) $constraint->maxWidth)) {
                throw new ConstraintDefinitionException(sprintf('"%s" is not a valid maximum width', $constraint->maxWidth));
            }

            if ($width > $constraint->maxWidth) {
                $this->context->addViolation($constraint->maxWidthMessage, array(
                    '{{ width }}'    => $width,
                    '{{ max_width }}' => $constraint->maxWidth
                ));

                return;
            }
        }
    }
}