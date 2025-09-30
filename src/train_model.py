from pycaret.datasets import get_data
from pycaret.regression import setup, create_model, save_model


# load dataset
insurance = get_data('insurance')

# init environment
s = setup(data = insurance, 
          target = 'charges', 
          session_id = 123,
          normalize = True,
          polynomial_features = True,
          bin_numeric_features= ['age', 'bmi'])

# train model (linear regression)
lr = create_model('lr')

# save model
save_model(lr, model_name = 'model/pycaret-model')

