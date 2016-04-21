class PhpDumper
{
    // ...

    private function addService($id, $definition)
    {
        $return = array();

        $return[] = '/**';
        if ($definition->isSynthetic()) {
            $return[] = ' * @throws RuntimeException always since this service is expected to be injected dynamically';
        } elseif ($class = $definition->getClass()) {
            $return[] = sprintf(" * @return %s A %s instance.", 0 === strpos($class, '%') ? 'object' : $class, $class);
        } elseif ($definition->getFactoryClass()) {
            $return[] = sprintf(' * @return object An instance returned by %s::%s().', $definition->getFactoryClass(), $definition->getFactoryMethod());
        } elseif ($definition->getFactoryService()) {
            $return[] = sprintf(' * @return object An instance returned by %s::%s().', $definition->getFactoryService(), $definition->getFactoryMethod());
        }

        $return[] = " */";

        $return[] = "public function get{$this->camelize($id)}Service()";
        $return[] = "{";

        $return[] = $this->addServiceBody($id, $definition);
        $return[] = "}";

        return implode("\n", $return);
    }

    // ...
}