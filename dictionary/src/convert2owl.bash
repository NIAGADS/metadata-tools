# convert niagads.obo to owl using robot https://github.com/ontodev/robot

robot convert --input ../obo/niagads.obo --output ../owl/niagadsobo.owl -vvv

# remove namespace niagadsobo# tag so that it will link terms when assembled into complete owl
sed -i 's/niagadsobo#//' ../owl/niagadsobo.owl
